import os
import requests
from urllib.parse import quote
import streamlit as st

def search_brave(query, api_key, count=10):
    """
    Perform a search using Brave Search API
    """
    base_url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }
    
    params = {
        "q": query,
        "count": count
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None

def display_search_result(result):
    """Display a single search result"""
    title = result.get('title', 'No Title')
    url = result.get('url', '#')
    description = result.get('description', 'No description available')
    
    st.markdown(f"### [{title}]({url})")
    st.markdown(f"<span style='color: green;'>{url}</span>", unsafe_allow_html=True)
    st.markdown(description)
    
    # Display additional meta information if available
    if 'meta' in result:
        meta = result['meta']
        if 'last_crawled' in meta:
            st.markdown(f"*Last crawled: {meta['last_crawled']}*")
    
    st.markdown("---")

def main():
    # Page configuration
    st.set_page_config(
        page_title="Brave Search",
        page_icon="🦁",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
        }
        .main {
            padding: 2rem;
        }
        h1 {
            color: #FB542B;
            text-align: center;
            margin-bottom: 2rem;
        }
        .search-container {
            margin: 2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.title("🦁 Brave Search")

    # API Key input
    api_key = st.text_input("Enter your Brave Search API Key", type="password")
    
    if not api_key:
        st.warning("Please enter your Brave Search API key to continue. You can get one from https://brave.com/search/api/")
        st.stop()

    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("Enter your search query", key="search_query")
    
    with col2:
        num_results = st.selectbox(
            "Number of results",
            [10, 20, 30],
            key="num_results"
        )

    # Search button
    if st.button("Search", type="primary"):
        if query:
            with st.spinner('Searching...'):
                results = search_brave(query, api_key, num_results)
                
                if results and 'web' in results:
                    web_results = results['web'].get('results', [])
                    
                    if web_results:
                        st.markdown(f"### Found {len(web_results)} results")
                        
                        # Display search metrics if available
                        if 'query' in results:
                            query_info = results['query']
                            st.markdown(f"*Search took {query_info.get('time_taken', 0)}ms*")
                        
                        # Display results
                        for result in web_results:
                            display_search_result(result)
                    else:
                        st.info("No results found")
                else:
                    st.error("Failed to get search results")
        else:
            st.warning("Please enter a search query")

    # Footer with API information
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; padding: 20px;'>
        Powered by Brave Search API | <a href="https://brave.com/search/api/" target="_blank">Get API Key</a>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()