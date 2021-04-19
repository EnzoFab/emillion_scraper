
# Euromillion scraper 

By using web scraping, the aim of the project is to get every euromillion results to do statistic over it.
To do so, we will use **selenium** package. 

```
pip install selenium
pip install pandas
pip install seaborn
pip install matplotlib
```

## Scraping

### Imports


```python
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
```

First we will get every page urls 
To do so, on the landing page and we get every href value of **a** tags, which contains a link to the draw history of a year


```python
url = "https://www.tirage-euromillions.net/euromillions/annees/"
options = Options()

# to hide the browser 
options.headless = True

browser = Firefox(options=options)
browser.get(url)

# get every tag 'a' in the 'li' tag
draws = browser.find_elements_by_xpath("//*[contains(@href, 'annee-20')]")

page_urls = []
for draw in draws:
    
    href = draw.get_attribute("href")
    
    page_urls.append(href)

#page_urls
```


```python
def extract_text_as_numb(elements: list) -> list:
    """
        get a list of int out of a list of HTML DOM
    """
    
    texts = []
    for el in elements:
        texts.append(int(el.text))
    return texts

def scrap_numbers(browser) -> list:
    """
        get a list of dict from a browser
    """
    
    css_selector = "tr"
    rows = browser.find_elements_by_tag_name(css_selector)
    
    trs = []
    for row in rows:
        try:
            # if the element doesn't contain a double td then drop this row
            # otherwise save it
            row.find_element_by_css_selector("td+td")
            trs.append(row)
        except:
            continue
    
    results = []
    for tr in trs:
        tds = tr.find_elements_by_tag_name("td")
        date = tds[0].text
        
        game_points = tr.find_elements_by_class_name("game_point")
        
        stars = tr.find_elements_by_class_name("star_small")
        
        line = {
            "date": date, 
            "numbers": extract_text_as_numb(game_points), 
            "stars": extract_text_as_numb(stars)
        }
        
        results.append(line)
    
    return results
```

Foreach page url, scrap the content and add it to the record. 

This action might take some times because scraping process is timeconsuming


```python
browser = Firefox(options=options)
euro_millions = []

for page_url in page_urls:
    browser.get(page_url)
    euro_millions += scrap_numbers(browser)
    
euro_millions[0:5]
```




    [{'date': 'Vendredi 16/04/2021',
      'numbers': [6, 11, 29, 40, 48],
      'stars': [5, 9]},
     {'date': 'Mardi 13/04/2021',
      'numbers': [16, 20, 31, 47, 50],
      'stars': [2, 8]},
     {'date': 'Vendredi 09/04/2021',
      'numbers': [2, 8, 32, 35, 44],
      'stars': [8, 11]},
     {'date': 'Mardi 06/04/2021', 'numbers': [2, 21, 37, 38, 50], 'stars': [7, 8]},
     {'date': 'Vendredi 02/04/2021',
      'numbers': [4, 21, 34, 40, 47],
      'stars': [2, 5]}]



Save the results as a csv file and we will be ready to work on our dataset.


```python
import csv
keys = euro_millions[0].keys()
with open('euro_million_history.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(euro_millions)
```

## Analysis

Using the dataset we just created, we are going to see if there are a miracle draw or a combinaison of numbers which often appears. 

Few questions in mind according to all of this. the question that all players ask themselves:
* **Is this game balanced ?**
* **Can we increase our chances of winning ?**

### imports


```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_theme(style="whitegrid")
```


```python
df = pd.read_csv("euro_million_history.csv")
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>numbers</th>
      <th>stars</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Vendredi 16/04/2021</td>
      <td>[6, 11, 29, 40, 48]</td>
      <td>[5, 9]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mardi 13/04/2021</td>
      <td>[16, 20, 31, 47, 50]</td>
      <td>[2, 8]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Vendredi 09/04/2021</td>
      <td>[2, 8, 32, 35, 44]</td>
      <td>[8, 11]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Mardi 06/04/2021</td>
      <td>[2, 21, 37, 38, 50]</td>
      <td>[7, 8]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Vendredi 02/04/2021</td>
      <td>[4, 21, 34, 40, 47]</td>
      <td>[2, 5]</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>numbers</th>
      <th>stars</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1416</td>
      <td>1416</td>
      <td>1416</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>1416</td>
      <td>1416</td>
      <td>124</td>
    </tr>
    <tr>
      <th>top</th>
      <td>Vendredi 14/11/2014</td>
      <td>[30, 26, 48, 15, 8]</td>
      <td>[2, 6]</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>1</td>
      <td>1</td>
      <td>25</td>
    </tr>
  </tbody>
</table>
</div>




```python
def prepare_numbers(dataframe, col_name:str) -> np.array:
    arr = np.array(dataframe[col_name].array)
    
    def cb(arg):
        res = arg.replace('[', '').replace(']', '').replace(',','')
        return np.array(res.split(' ')).astype(int)
    
    return np.array(list(map(cb, arr))).flatten()
          
```


```python
numbers = prepare_numbers(df, "numbers")
stars = prepare_numbers(df, "stars")

stars
```




    array([5, 9, 2, ..., 5, 6, 5])




```python
plt.figure(figsize=(20,20))
plt.hist(numbers, bins=100)
plt.gca().set(title='Number histogram', ylabel='Nb of occurence')

```




    [Text(0, 0.5, 'Nb of occurence'), Text(0.5, 1.0, 'Number histogram')]




![png](notebook/images/output_17_1.png)



```python
(unique, counts) = np.unique(numbers, return_counts=True)
occurence = np.asarray((unique, counts)).T
np.sort(occurence, axis=1)

# sort by number of occurence
sorted_occurence = sorted(occurence, key=lambda row: row[1])

count = df.shape[0]

df_numbers = pd.DataFrame((list(map(lambda x: {"number": x[0], "frequencies": (x[1]/count) * 100} ,sorted_occurence))))
df_numbers.tail(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>frequencies</th>
      <th>number</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>45</th>
      <td>11.087571</td>
      <td>37</td>
    </tr>
    <tr>
      <th>46</th>
      <td>11.158192</td>
      <td>19</td>
    </tr>
    <tr>
      <th>47</th>
      <td>11.440678</td>
      <td>50</td>
    </tr>
    <tr>
      <th>48</th>
      <td>11.511299</td>
      <td>44</td>
    </tr>
    <tr>
      <th>49</th>
      <td>11.581921</td>
      <td>23</td>
    </tr>
  </tbody>
</table>
</div>




```python
plt.figure(figsize=(20,15))
ax = sns.barplot(data=df_numbers, x="number", y="frequencies", order=df_numbers["number"], estimator=np.median)
ax.set(xlabel='Number', ylabel='Frequency (%)')
ax.set_ylim([0,15])
plt.show()
```


![png](notebook/images/output_19_0.png)


The chart above show us that with almost 1500 lines, the distribution of the frequencies is close to uniform. Each numbers has a frequency greater than 8% and lower than 12%

Even if some numbers appear more often than the other ones, the difference isn't significative enough to get a trend. So unfortunetly, it seems that there isn't a magic trick.

Yet, to go further we can pick a random number a see which of the other numbers are more likely to get you a win (according to the winning combinaisons)


```python
(unique, counts) = np.unique(stars, return_counts=True)
frequencies = np.asarray((unique, counts)).T
np.sort(frequencies, axis=1)
sorted_frequencies = sorted(frequencies, key=lambda row: row[1])

df_stars = pd.DataFrame(
    list(
        map(lambda x: {"number": x[0], "count": x[1]} ,sorted_frequencies)
    )
)

df_stars.tail(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
      <th>number</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>7</th>
      <td>260</td>
      <td>5</td>
    </tr>
    <tr>
      <th>8</th>
      <td>266</td>
      <td>9</td>
    </tr>
    <tr>
      <th>9</th>
      <td>283</td>
      <td>3</td>
    </tr>
    <tr>
      <th>10</th>
      <td>285</td>
      <td>8</td>
    </tr>
    <tr>
      <th>11</th>
      <td>289</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>




```python
plt.figure(figsize=(20,15))
ax = sns.barplot(data=df_stars, x="number", y="count", order=df_stars["number"], estimator=np.median)
ax.set(xlabel='Star', ylabel='Nb of occurence')
plt.show()
```


![png](notebook/images/output_22_0.png)


Contrary to the histogram of the numbers, we can see here a more significative difference in the number of apparence. The star eleven doesn't appear a lot. So if you follow the trend, we shouldn't bet on the 12 nor 11 or 10 stars if we want to maximise our chance to win


```python

```
