# Medium-GraphQL-Post-API
> A web scraper for retrieving Medium posts using GraphQL API

A Python script for retrieving Medium posts using GraphQL API. This script can be used to scrape Medium posts based on search queries or by the author's username.

![](header.png)

## Installation

```sh
pip 
```

## Usage example

Using get_posts_by_tag method

```sh
mymedium_api = Medium_GraphQL_Post_API()
posts = mymedium_api.get_posts_by_tag(tag="python",mode="HOT",limit=1,start=0)
print(posts)
```

Result :
```sh
[Post(
title='Mastering Next-Level Web Automation with Python and Selenium',
subtitle='Have you ever found yourself waiting for a web page to load or a button to become clickable while working on a Selenium automation project…',
link='https://medium.com/@musowir_u/advanced-web-automation-techniques-with-selenium-and-python-790e0446a325',
publishing_datetime='2023-02-21 16:36:43',
last_edit_datetime='2023-02-21 19:18:03',
reading_time_in_minutes='3 min',
rating=103,
tags=['selenium', 'web-automation', 'automation', 'selenium-webdriver', 'python'],
image='https://miro.medium.com/fit/c/400/400/1*CpUGCCe5yYvflqwFZ1iRdQ.png',
creator_name='Abdu Musowir U',
creator_username='musowir_u',
post_preview_title='Mastering Next-Level Web Automation with Python and Selenium',
post_preview_sub_title='',
post_preview_description='Have you ever found yourself waiting for a web page to load or a button to become clickable while working on a Selenium automation project? If you have, then you know how frustrating it can be to have your automation script fail just because you didn’t wait long enough for…',
post_preview_image='https://miro.medium.com/fit/c/400/400/1*CpUGCCe5yYvflqwFZ1iRdQ.png')]
```




Using search_posts method

```sh
mymedium_api = Medium_GraphQL_Post_API()
search = mymedium_api.search_posts(search="artificial intelligence",limit=1,start=0)
print(search)
```

Result :
```sh
[Post(
title='How I Eat For Free in NYC Using Python, Automation, Artificial Intelligence, and Instagram', subtitle='Living and working in the big apple comes with big rent.',
link='https://medium.com/@chrisbuetti/how-i-eat-for-free-
in-nyc-using-python-automation-artificial-intelligence-and-instagram-a5ed8a1e2a10',
publishing_datetime='2019-02-24 20:58:27',
last_edit_datetime='2021-06-03 21:53:03',
reading_time_in_minutes='21 min',
rating=11615,
tags=['social-media', 'python', 'instagram', 'data-science', 'automation'],
image='https://miro.medium.com/fit/c/400/400/1*MG74B8MQ9R4okdwBl_SkMg.png',
creator_name='Chris Buetti', creator_username='chrisbuetti',
post_preview_title='How I Eat For Free in NYC Using Python, Automation, Artificial Intelligence, and Instagram',
post_preview_sub_title='',
post_preview_description='I, along with most other city-dwellers who live inside a crammed closet we call an apartment, look to cut costs anywhere we can. It’s no secret one way to curtail expenses, at least we’re told, is to cook at…',
post_preview_image='https://miro.medium.com/fit/c/400/400/')]

```
## Want to Support Me ?

<a href="https://www.buymeacoffee.com/irvhes3" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>


## Release History

* 0.1.0
    * The first proper release
    * Comment the whole code
    * Create the Github Page
    
* 0.0.1
    * Work in progress

