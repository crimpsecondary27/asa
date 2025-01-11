import streamlit as st
from duckduckgo_search import DDGS
import time

def perform_search(query, search_type="text", max_results=10):
    """
    Perform a search using DuckDuckGo
    """
    with DDGS() as ddgs:
        try:
            if search_type == "text":
                results = list(ddgs.text(query, max_results=max_results))
            elif search_type == "image":
                results = list(ddgs.images(query, max_results=max_results))
            elif search_type == "news":
                results = list(ddgs.news(query, max_results=max_results))
            elif search_type == "video":
                results = list(ddgs.videos(query, max_results=max_results))
            return results
        except Exception as e:
            st.error(f"Search error: {str(e)}")
            return []

def display_text_result(result):
    """
    Display a text search result with title, link, and snippet
    """
    st.markdown(f"### [{result['title']}]({result['link']})")
    st.markdown(f"<span style='color: green;'>{result['link']}</span>", unsafe_allow_html=True)
    st.markdown(result['body'])
    st.markdown("---")

def display_image_result(result):
    """
    Display an image search result
    """
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(result['image'], width=150)
    with col2:
        st.markdown(f"### [{result['title']}]({result['link']})")
        st.markdown(f"<span style='color: green;'>{result['link']}</span>", unsafe_allow_html=True)
    st.markdown("---")

def display_news_result(result):
    """
    Display a news search result
    """
    st.markdown(f"### [{result['title']}]({result['link']})")
    st.markdown(f"<span style='color: green;'>{result['link']}</span>", unsafe_allow_html=True)
    st.markdown(f"*{result['date']}*")
    st.markdown(result['body'])
    st.markdown("---")

def display_video_result(result):
    """
    Display a video search result
    """
    st.markdown(f"### [{result['title']}]({result['link']})")
    st.markdown(f"<span style='color: green;'>{result['link']}</span>", unsafe_allow_html=True)
    if 'description' in result:
        st.markdown(result['description'])
    st.markdown(f"Duration: {result.get('duration', 'N/A')}")
    st.markdown("---")

def main():
    # Set page config
    st.set_page_config(
        page_title="DuckDuckGo Search",
        page_icon="🔍",
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
            color: #DE5833;
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.title("🔍 DuckDuckGo Search")

    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("Enter your search query", key="search_query")
    
    with col2:
        search_type = st.selectbox(
            "Search type",
            ["text", "image", "news", "video"],
            key="search_type"
        )

    num_results = st.slider("Number of results", 5, 30, 10)

    # Search button
    if st.button("Search", type="primary"):
        if query:
            # Show spinner while searching
            with st.spinner('Searching...'):
                results = perform_search(query, search_type, num_results)
                
                # Display results based on search type
                if results:
                    st.markdown(f"### Found {len(results)} results")
                    for result in results:
                        if search_type == "text":
                            display_text_result(result)
                        elif search_type == "image":
                            display_image_result(result)
                        elif search_type == "news":
                            display_news_result(result)
                        elif search_type == "video":
                            display_video_result(result)
                else:
                    st.info("No results found")
        else:
            st.warning("Please enter a search query")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; padding: 20px;'>
        Made with Streamlit and duckduckgo-search
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()