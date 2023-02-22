from requests_html import HTMLSession
from bs4 import BeautifulSoup

def get_medium_posts(tag,mode='trending',time='week'):    
    mode_dict = {
        "top": "https://medium.com/tag/{}/top/{}".format(tag,time),
        "latest": "https://medium.com/tag/{}/latest".format(tag),
        "trending": "https://medium.com/tag/{}".format(tag)
    }  
    session = HTMLSession()          
    req = session.get(mode_dict[mode])
    
    
    
    #extract all tag articles from the page
    soup = BeautifulSoup(req.text, 'html.parser')
    articles = soup.find_all('article', class_='meteredContent')
    #extract the title in h2 tag
    article_dict = {}
    
    #Bypass the medium obfuscation
    for article in articles:
        title = article.find('h2')
        #get the all paragraphs
        paragraphs = article.find_all('p')           
        author = paragraphs[0].text
        #get an a element in article with attribute aria-label="Post Preview Title" and get the href of the a element
        link = "https://medium.com" +  article.find('a', attrs={'aria-label':'Post Preview Title'})['href'].split('?')[0]
        
        #get an img element in article with attribute loading="lazy" and get the src of the img element with width=112 and height = 112
        low_image = article.find('img', attrs={'loading':'lazy', 'width':'112', 'height':'112'})['src']
        
        print(title.text)
        # low_image = article.find('img', attrs={'alt':title.text})['src']        
        low_image.replace('w=112&h=112','w=400&h=400')
        print(low_image)
        input()
        for p in paragraphs:
        #     if "ago" in p.text:
        #         published_time = p.text
        #     if "read" in p.text:    
        #         time_to_read = p.text
            if len(p.text) >15:
                description = p.text
        # 'published_time': published_time,

            
        article_dict[title.text] = {
            'author': author,
            'source': 'medium',
            # 'time_to_read': time_to_read,
            'description': description,
            'link': link,
            'icon': low_image
        }
    return article_dict      

