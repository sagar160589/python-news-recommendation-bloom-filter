#News Recommendation using bloom filter

This project focuses on displaying news recommendations to users based using bloom filters data structure. Bloom filter is a probablistic 
data structure which accurately tells if an element is not present in it but probably tells if an element is present.
More on bloom filters : - https://en.wikipedia.org/wiki/Bloom_filter

In this we have scraped a news website to get the news titles and then created a bloom filter inside Redis in-memory which tells us if a news is to be recommended to the user if its entry is DEFINITELY not present in the bloom filter.
And it also gives false positives which mentions that a news is not to be recommended to the user even if its entry is not present in the bloom filter.

This code can be further optimized to use flask if we want the news recommendation is to be shown on a webpage to the user.

P.S - This is a standalone utility which is created to show news recommendations to the user