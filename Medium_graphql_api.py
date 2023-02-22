import json
from dataclasses import dataclass
from datetime import datetime
import requests
from typing import List

@dataclass
class Post:
    title: str
    subtitle:str
    link: str
    publishing_datetime:str
    last_edit_datetime: str
    reading_time_in_minutes: str    
    rating: int
    tags: list
    image: str
    creator_name: str
    creator_username: str
    post_preview_title: str
    post_preview_sub_title: str
    post_preview_description: str
    post_preview_image: str

class Medium_GraphQL_Post_API:
    """
    A web scraper for retrieving Medium posts.
    by Osyna
    """
        
    def __init__(self,Local : bool = False):
        """
        Initializes the MediumScraper object.
        """
        
        self.session = requests.Session()   # Init a session
        self.medium_url = 'https://medium.com' # Define Medium.com URL
        self.medium_cdn = 'https://miro.medium.com' # Define Medium CDN URL
        
        # Error handling if Medium.com or Medium CDN is down
        try:
            #Test if Medium.com is up / reachable / Ip is not blocked
            if self.session.get(self.medium_url).status_code != 200:
                raise Exception('Medium.com is down')         
        
            # Test if Medium CDN is up / reachable / Ip is not blocked
            if self.session.get(self.medium_cdn).status_code != 200:
                raise Exception('Medium CDN is down')
        except:
            raise Exception('Medium.com or Medium CDN is down or your IP is blocked')
        
        if Local:        
            # Load the GraphQL Queries from the files
            # read the file in the folder named medium_graph_ql_post_by_tag.req
            with open('medium_graph_ql_post_by_tag.req', 'r') as f:
                self.graph_ql_post_by_tag_query = f.read()

            # read the file in the folder named medium_graph_ql_search.req
            with open('medium_graph_ql_search.req', 'r') as f:
                self.graph_ql_search_posts_query = f.read()
        else:
            try:
                self.graph_ql_search_posts_query = self.session.get('https://raw.githubusercontent.com/Osyna/Medium-GraphQL-Post-API/main/medium_graph_ql_search.req').text
                self.graph_ql_post_by_tag_query = self.session.get('https://raw.githubusercontent.com/Osyna/Medium-GraphQL-Post-API/main/medium_graph_ql_post_by_tag.req').text
            except:
                raise Exception('Cannot use distant req files. Please download the req files and set Local to True')

               
        # Define Default User Agent, can be easily changer by the user calling set_user_agent() function
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
        
        # Define Default Headers with default graphql-operation = TopicFeedQuery
        self.headers = {
                    'User-Agent': self.user_agent,
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'content-type': 'application/json',
                    'graphql-operation': 'TopicFeedQuery',
                    'Origin': 'https://medium.com'
        }      
    
        # Set Default Image Size
        image_size = 400        
        self.medium_cdn_image = f'{self.medium_cdn}/fit/c/{image_size}/{image_size}/%s'

    def set_user_agent(self,user_agent:str):
        """_summary_: Set the User Agent for the requests

        Args:
            user_agent (str): User Agent to use for the requests
        """
        
        self.user_agent = user_agent
        self.headers['User-Agent'] = user_agent

    def set_image_size(self,width : int,height :int) -> None:
        """_summary_: Set the Image Size for the requests
        
        Args:  
            width (int): Width of the image
            height (int): Height of the image         
        """
        
        self.medium_cdn_image = f'{self.medium_cdn}/fit/c/{width}/{height}/%s'
    
    def get_posts_by_tag(self, tag: str, mode: str, limit: int = 10, start: int = 0) -> List[Post]:
        """
        Return a list of all posts that have the given tag.

        Args:
            posts (list of dict): A list of post dictionaries.
            tag (str): The tag to filter the posts by.
            mode (str): The mode to use for sorting the posts. Must be one of HOT, NEW, TOP_WEEK, TOP_MONTH, TOP_YEAR, or TOP_ALL_TIME.
            limit (int): The maximum number of posts to return. Defaults to 10.
            start (int): The starting index of the posts to return. Defaults to 0.

        Returns:
            list of dict: A list of post dictionaries that have the given tag.
        """               
        
        # Raise an exception if the mode is not valid.        
        if mode not in ['HOT' , 'NEW', 'TOP_WEEK', 'TOP_MONTH', 'TOP_YEAR', 'TOP_ALL_TIME']:
            raise Exception('Mode must be one of the following: HOT , NEW, TOP_WEEK, TOP_MONTH, TOP_YEAR, TOP_ALL_TIME')       
        
        self.headers['graphql-operation'] = 'TopicFeedQuery' # Set the GraphQL operation header to "TopicFeedQuery"     
        
        # Format the data for the GraphQL API call.
        data =  """
        [{
            "operationName":"TopicFeedQuery",
            "variables":{"tagSlug":"%s",
            "mode":"%s",
            "paging":{
                "to":"%s",
                "limit":%s
                }
            },
            "query":"%s"
        }]""" % (tag,mode,start,limit,self.graph_ql_post_by_tag_query)
         
        # Make a POST request to the Medium API endpoint with the constructed GraphQL query and headers
        response = self.session.post('https://medium.com/_/graphql', headers=self.headers, data=data)
        
        # Check if the response is a Bad Request error
        if response.text == "Bad Request":
            raise Exception("Bad Request Response from Medium. The API Might have changed. Please contact the developer trough Github.")      
        
        parsed_resp = json.loads(response.text) # Parse the response as JSON     
        items = parsed_resp[0]['data']['tagFeed']['items']   # Extract the items from the response   
        Posts_list = [] # Init a list to store the posts
                
        # Loop through the items and extract the data
        for i_data in items:
            post_data = i_data['post']
            creator_data = post_data['creator']
            creator_name = creator_data['name']
            creator_username = creator_data['username']   
                        
            publishing_datetime = datetime.fromtimestamp((post_data['firstPublishedAt'])/1000).strftime('%Y-%m-%d %H:%M:%S') # Convert the timestamp to datetime
            last_edit_datetime = datetime.fromtimestamp((post_data['latestPublishedAt'])/1000).strftime('%Y-%m-%d %H:%M:%S')  # Convert the timestamp to datetime
                           
            reading_time_in_minutes = str(post_data['readingTime']).split('.')[0] + " min"
            post_title = post_data['title']
            post_link = post_data['mediumUrl']
            rating = post_data['clapCount']
            subtitle = post_data['extendedPreviewContent']['subtitle']            
            post_preview_data = post_data['extendedPreviewContent']['bodyModel']['paragraphs']     
            preview_title, preview_sub_title,preview_image,preview_description = "","","",""
            
            # Loop through the post preview data and extract the data
            for d in post_preview_data:
                if d['type'] == 'IMG':
                    preview_image = d['metadata']['id']        
                if d['type'] == 'H3':
                    preview_title = d['text']
                if d['type'] == 'H4':
                    preview_sub_title = d['text']                            
                if d['type'] == 'P' and len(d['text'])>len(preview_description) : # Get the longest paragraph
                   preview_description = d['text']
            
            # Extract the tags       
            tags = [t['normalizedTagSlug'] for t in post_data['tags']]      
            
            # Format the image URLs      
            image = post_data['previewImage']['id']           
            image = self.medium_cdn_image % image
            preview_image = self.medium_cdn_image % preview_image
            
            # Append the post to the list
            Posts_list.append(Post(title=post_title,
                                   subtitle=subtitle,
                                   link=post_link,
                                    publishing_datetime=publishing_datetime,
                                    last_edit_datetime=last_edit_datetime,
                                    reading_time_in_minutes=reading_time_in_minutes,
                                    rating=rating,
                                    tags=tags,
                                    image=image,
                                    creator_name=creator_name,
                                    creator_username=creator_username,
                                    post_preview_title=preview_title,
                                    post_preview_sub_title=preview_sub_title,
                                    post_preview_description=preview_description,
                                    post_preview_image=preview_image
                                    ))
        return Posts_list                              

    def search_posts(self, search: str, limit: int = 10, start: int = 0) -> List[Post]:
        """Searches Medium for posts based on a search query.

        Args:
            search (str): The search query.
            limit (int, optional): The maximum number of results to return. Defaults to 10.
            start (int, optional): The starting index of the results. Defaults to 0.

        Returns:
            List[Post]: A list of Post objects matching the search query.
        """
        
        # Set the GraphQL operation header to SearchQuery       
        self.headers['graphql-operation'] = 'SearchQuery'      
        
        # Construct the GraphQL query with the search keyword, limit, start, and other options
        data = """
        [{
            "operationName": "SearchQuery",
            "variables": {
                "query": "%s",
                "pagingOptions": {
                    "limit": %s,
                    "page": %s
                },
                "withUsers": false,
                "withTags": false,
                "withPosts": true,
                "withCollections": false,
                "withLists": false,
                "peopleSearchOptions": {
                    "filters": "highQualityUser:true OR writtenByHighQulityUser:true",
                    "numericFilters": "peopleType!=2",
                    "clickAnalytics": true,
                    "analyticsTags": ["web-main-content"]
                },
                "postsSearchOptions": {
                    "filters": "writtenByHighQualityUser:true",
                    "clickAnalytics": true,
                    "analyticsTags": ["web-main-content"]
                },
                "publicationsSearchOptions": {
                    "clickAnalytics": true,
                    "analyticsTags": ["web-main-content"]
                },
                "tagsSearchOptions": {
                    "numericFilters": "postCount>=1",
                    "clickAnalytics": true,
                    "analyticsTags": ["web-main-content"]
                },
                "listsSearchOptions": {
                    "clickAnalytics": true,
                    "analyticsTags": ["web-main-content"]
                },
                "searchInCollection": false,
                "collectionDomainOrSlug": "medium.com"
            },
            "query": "%s"
        }]
        """ % (search, limit, start, self.graph_ql_search_posts_query) 
                
        # Make a POST request to the Medium API endpoint with the constructed GraphQL query and headers
        response = self.session.post('https://medium.com/_/graphql', headers=self.headers, data=data)
        
        # Check if the response is a Bad Request error
        if response.text == "Bad Request":
            raise Exception("Bad Request Response from Medium. The API Might have changed. Please contact the developer trough Github.")         
        
        # Parse the JSON response
        parsed_resp = json.loads(response.text)             
        
        # Extract the posts from the parsed response
        items = parsed_resp[0]['data']['search']['posts']['items']

        # Create a list to hold the Post objects
        Posts_list = []
        
        # Loop through the post items and extract relevant data to create a Post object
        for i_data in items:           
            creator_data = i_data['creator']                
            creator_name = creator_data['name']
            creator_username = creator_data['username']                 
            publishing_datetime = datetime.fromtimestamp((i_data['firstPublishedAt'])/1000).strftime('%Y-%m-%d %H:%M:%S') # Convert the timestamp to datetime
            last_edit_datetime = datetime.fromtimestamp((i_data['latestPublishedAt'])/1000).strftime('%Y-%m-%d %H:%M:%S')  # Convert the timestamp to datetime            
            reading_time_in_minutes = str(i_data['readingTime']).split('.')[0] + " min"
            post_title = i_data['title']
            post_link = i_data['mediumUrl']
            rating = i_data['clapCount']            
            subtitle = i_data['extendedPreviewContent']['subtitle']
            post_preview_data = i_data['extendedPreviewContent']['bodyModel']['paragraphs']     
            preview_title, preview_sub_title,preview_image,preview_description = "","","",""

            # Extract the preview data for the post
            for d in post_preview_data:
                if d['type'] == 'IMG':
                    preview_image = d['metadata']['id']        
                if d['type'] == 'H3':
                    preview_title = d['text']
                if d['type'] == 'H4':
                    preview_sub_title = d['text']                            
                if d['type'] == 'P' and len(d['text'])>len(preview_description) :
                   preview_description = d['text']
             
            # Get the tags for the post       
            tags = [t['normalizedTagSlug'] for t in i_data['tags']]            
            
            # Get the cover image for the post
            image = i_data['previewImage']['id']
            
            # Format the image URLs
            image = self.medium_cdn_image % image
            preview_image = self.medium_cdn_image % preview_image
            
            # Create a Post object and append it to the list
            Posts_list.append(Post(title=post_title,
                                   subtitle=subtitle,
                                   link=post_link,
                                    publishing_datetime=publishing_datetime,
                                    last_edit_datetime=last_edit_datetime,
                                    reading_time_in_minutes=reading_time_in_minutes,
                                    rating=rating,
                                    tags=tags,
                                    image=image,
                                    creator_name=creator_name,
                                    creator_username=creator_username,
                                    post_preview_title=preview_title,
                                    post_preview_sub_title=preview_sub_title,
                                    post_preview_description=preview_description,
                                    post_preview_image=preview_image
                                    ))
        return Posts_list                              
