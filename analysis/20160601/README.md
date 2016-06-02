# TR Analysis
# June 1, 2016
Discussion
Summary: Learn to dig deep into your original dataset. Clean your data before you start experiments.
         Find something uncommon and try to find its answer.

The recommendation results are given in "precisionWithRatingTimes.txt"


Q: What's next step?
A: Try to find something uncommon in the results and look into the original data.

Q: But there are 4000 records......
A: Yes, Nobody wants to go over 4000 records manually. However, we don't need go over all the records.
   Just CHOOSE SEVERAL SPECIAL RECORDS
   
Q: WHERE is the SPECIAL RECORDS?
A: Special... Look at the 3rd record (line 4). In trainning dataset, there are only 5 ratings. But, 
   why the hit-rate is so high (49/50)? If "50" means the length of the candidate list, why 49 out of
   50 movies are accepted? In what condition can this situation happen?
   
A: Look at the record at line 2175. User 5927's rating number exceeds 200, and his rating time-span 
   is more than 200 days. However, why there is no correct recommendations in even 50-long candidate
   list?

Q: There are so many users with 0% hit-rate, more than 4000. It's common
A: Why it's common? It's uncommon. Why are there so many 0% hit-rate? The fact may lie in the splition
   of training dataset and testing dataset. If the dataset is cut into two parts just according to a
   certain date, some users' datasets will be wholely put into training dataset and there is NO data
   in testing dataset. Thus the hit-rate will be total 0%

Q: Somebody who studied this topic had said that splitting the dataset by time point is the only correct
   way.
A: Did he give proof for his opinion? Is there a paper describe this topic? If not, don't treat it as
   a truth.   
