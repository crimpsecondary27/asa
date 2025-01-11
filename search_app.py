import streamlit as st
import requests

# Function to perform search using Brave Search API
def perform_search(query, search_type="text", max_results=10):
    """
    Perform a search using Brave Search API
    """
    api_url = "https://api.brave.com/search"  # Brave Search API endpoint
    headers = {
        "Authorization": "Bearer BSAYheekFJaSF7P3QDGHUyJQnCFahzW",  # Replace with your Brave API key
    }

    params = {
        "q": query,
        "count": max_results,
        "type": search_type  # text, image, video, or news
    }

    try:
        # Adding timeout to prevent hanging indefinitely
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes (4xx, 5xx)
        data = response.json()  # Get JSON response
        return data.get('results', [])
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again later.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Search error: {str(e)}")
        return []

# Functions to display results
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
        page_title="Brave Search",
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
    st.title("🔍 Brave Search")

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
        Made with Streamlit and Brave Search API
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
