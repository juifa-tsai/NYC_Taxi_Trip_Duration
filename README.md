# [Kaggle] New York texi-trip duration

*<div style="text-align: center;" markdown="1">`EDA` `regression` `clustering` `scikit-learn` `numpy` `pandas`</div>*

## Introduction
This is the [competition](https://www.kaggle.com/c/nyc-taxi-trip-duration) of the machine learning. The data is the travel information for the New York texi. The prediction is using the **regression** method to predict the trip duration depending on the given variables. The variables contains the locations of pickup and dropoff presenting with latitude and longitude, pickup date/time, number of passenger etc.... The design of the learning algorithm includes the preprocess of feature explaration and data selection, modeling and validation. To improve the prediction, we have done several test for modeling and feature extraction. Here we give the summery of the results.   

<div style="text-align: center;" markdown="1"><img src="https://i.imgur.com/SESNTXJ.jpg" height="250"></div>

## Techniques
The procedure in this study includes the [feature exploration](#1-feature-exploration), [clustering](#2-clustering) and [modeling](#3-modeling). The feature selection is dealing with the noice which is possible to contaminate the prediction. Since less of the domain knowledges, the data was selected by visiulizing the data and observed the distribution of each features. The following figuresshows the pickup location from the training data.

### 1. Feature exploration
The features in dataset are actually less, and some of them are noisy during the data-taking. Before training the model, it is better to explore the much useful feature and veto the noise. However, we believe those relevant information is hiding behind the data, e.g. the distance, direction or density, we made several statistical studies to extract those additional features. Except for searching from the original data, the extra knowledge is also added for the model trianing which is from the other studies by the expert of this domain. These studies, called ***explanatory data analysis (EDA)*** , improve the final prediction of the trained model. The summerized selection is as following list, and the details are described in the subsections. 
 
- 300 < Trip duration < 7200 (sec.)
- Veto date : 2016.01.20 ~ 2016.01.25
- 0.6 < Distance < 11 (Km)
- 5 < speed < 120 (Km/hr)
- 1 < Number of passenger < 7

#### 1.1. Time and duration
The pickup datatime is recored in both training and test dataset, while the dropoff and duration are only shown in training dataset. We analyzed the datetime by observing the distribution of month, week, day and the clock. The distrubtion of date shows the strange drop between January 20th to 25th, since the big snow was in New York which course the trafic problem. 

<div style="text-align: center;" markdown="1"><img src="https://i.imgur.com/wE36EGn.png" height="200"></div>


On the other hand, the training data with the large duration is discarded by the observation, since we believe those data are the outlier from the prediction for New York City. The selection is set larger than 2 minute and lower than 2 hours.   

#### 1.2. Distance, speed and direction 
The locations, speed and direction are expected to be strongly correlated to duration, especially the distance. We can use the coordinates of each pickup and dorpoff to overlook the scattering map of New York City. The important feature quickly shown up is the densities of pickup and dropoff location. 

<div style="text-align: center;" markdown="1"><img src="https://i.imgur.com/LcXLVn1.png" height="300"></div>

The most of dense regions are in the city center and two airports. The direction from pickup to dropoff may point out the popular locations, especailly bewteen city center to airport, which can effect the duration prediction. Thus, we estimated the direction as

<div style="text-align: center;" markdown="1"><img src="https://i.imgur.com/5BQDR2i.png" height="300"></div>

Moreover, the distance between dropoff and pickup are calculated with *haversine* distance, i.e. 

$$
d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}\ ,
$$ 

where it presents the distance between point 2 to 1. From the distrubtion, we found that a few of training data are out of the New York city, and the distance are extremely large. Thus, we only consider the data containing the distance in the coverage of 95% of the training dataset, assuming the distribution of distance is the gaussian distribution. In the end, there are duration information in training dataset, we simply calculated the average speed. The speed information provide the information of the noisy data. The data containing the speed between 5 and 120 (km/hr) are only used for training.

#### 1.3. Passenger

According the distrubtion of passengers, it appears the overcounting issue which is out of the normal texi's capacity. Thus, the data has to be appilied the selection of passengers between above 0 and less than 7.

#### 1.4. Extra feature - right/left turns
By adding the extra data, [Open Source Routing Machine (OSRM)](https://www.kaggle.com/oscarleo/new-york-city-taxi-with-osrm/kernels), it gives the additional information about the traffic for each route of data. Here we use the steps of the turns during the texi driving for model training, i.e. the number of right and left turns. The turn is expected to affect duration, since the time cost for right and left turn is different. For the *right-hand traffic (RHT)* city, e.g. New York City and Taipei, the right turn is much efficient than the left turn, hence the duration with less left turns is much smaller with respect to the same distance. 

### 2. Clustering
We have studied the different clustering algorithms to quantify or labelize the pickup and dropoff locations, e.g. the ***k-means*** algorithm and ***density pixels*** which made by statistical studies. Since the limited competition dateline and manpower, the ***density pixels*** wasn't compeletily finished, the performance is similar with *k-mean* algorithm for the choosen training model. Thus, the final prediction is using *k-means* to do feature extraction.

#### 2.1. K-means
The ***k-means*** algorithm one of choise to ensemble the data and labelizes the locations. The important feature of the algorithm is it is clustering the data by looking for the *k* clusters (sets), which the data in the set has the minimum error with respect to set's mean. In the case for clustering the locations by the coordinates, it can represent the *k* regions having different density. However, we didn't optimize the number of cluster, the value of regions is set 100. The following left-hand figure shows the coverage regions in prediction. The left-hand figure shows the clustering results applied to data.

<div style="text-align: center;" markdown="1"><img src="https://i.imgur.com/vZH0haY.png" height="300"><img src="https://i.imgur.com/rS8uXYG.png" height="320"></div> 

#### 2.2. Density pixels
The method is trying to give the meaningful value for training models instead of labelizing. By using the physics sence, we caculate the density from the pickup and dropoff cooredinates with respect to the fixed bin sizes of maps, we call they are *"pixels"*. Each pixel has different value which present how often the texi pickup and dropoff in the region. The results can be shown as heat map as following figure; the right-hand figures present in the linear scale, while the left-hands present log scale; the top figures are for the pickup cases, while the bottoms are for the dropoff cases.

<div style="text-align: center;" markdown="1"><img src="https://i.imgur.com/XBYu30C.png" height="500"></div>

Of course, the bin size can optimize as a supper parameter of clustering. We can expected either the large or the small bin sizes may give the missleading of the model training. The interesting feature we have found, the density difference between pickup and dropoff presnt with nomal distrubtion as following figure.

<div style="text-align: center;" markdown="1"><img src="https://i.imgur.com/QiHLVpR.png" height="250"></div>

It shows there is the certain frequence of trips between two regions. Thus, we take the absolute value of the difference and comparing the duration as the following figure.

<div style="text-align: center;" markdown="1"><img src="https://i.imgur.com/ySW9vxr.png" height="300"></div>

The correlation tells the story, which can be easily understood, the long duration is most from the city center to not popular region, while the short duration can be inside the city center where the densities almost in common. On the orther hand, we also cauclate the average speed in each region which the average speed can give the expectation of the duration. However, this method is pushing to human learning by statistical analysis instead of the machine learning, we didn't go deep in the end.

### 3. Modeling
Since the dimension of provided features in data is  not many, and the data is noisy, we decided use the ***tree*** learning algorithm as the training model. Two tree algorithms, **random forest** and **boosted decision tree (BDT)**, have been compared, BDT is used for our final fit. As metioned in begin of [clustering](#2-Clustering), the *k-means* algorithm is used for location imformation, since labelization algorithm does not need to be apllied one-hot-code for tree algorithm. It make the [*k-means*](#21-K-means) is much easier to be implemented than *density pixel* method. 

The public ***RMSLE*** score of the model without applying the [*OSRM*](#14-Extra-feature---rightleft-turns) is 0.39, and it is improved to 0.38 after the application. The *RMSLE* score, i.e. *Root Mean Squared Logarithmic Error*, is defined as

$$
\epsilon_{RMSLE}=\sqrt{\frac{1}{n}\sum_{i=1}^n\left(\ln(p_i+1)-\ln(a_i-1)\right)^2}\ ,
$$

where $n$ is the total number of observations in the dataset; $p_i$ is the prediction, while $a_i$ is the actual value. 

The model is validated by checking the learning curve between test and training dataset with **n-fold cross validation**, it shows no overfitting issue exist. The training epoch is shown in following figure. 
<div style="text-align: center;" markdown="1"><img src="https://i.imgur.com/iv1MYmF.png" height="400"></div>

<!-- kernel svm regression + stokastic -->

## Results
The final $\epsilon_{RMSLE}$ on Kaggle private dataset is 0.37. The score is in the top %8 of 1257 teams. Obviously, the results still can be improved by modeling or feature exploration.

## Reference
- [Kaggle - New York City Taxi Trip Duration](https://www.kaggle.com/c/nyc-taxi-trip-duration)
- Team Github : https://github.com/yennanliu/NYC_Taxi_Trip_Duration
- Personal Github : https://github.com/juifa-tsai/NYC_Taxi_Trip_Duration
- [Calculate distance, bearing and more between Latitude/Longitude points](https://www.movable-type.co.uk/scripts/latlong.html)
