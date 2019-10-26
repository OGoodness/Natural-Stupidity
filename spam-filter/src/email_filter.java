/*package main.spamfilter;*/

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

/**
 * tool class for reading input files
 * @author Junxiu Zhou
 *
 */
public class email_filter {
	
	Map<String, Integer> wordMap = new HashMap<String, Integer>();
	static List<String> commonMap = new LinkedList<String>();
	/**
	 * the features you want to use
	 * you can customize this by yourself
	 * the maximum possible is plotted in the Console
	 */
	int most_common = 100; 
	int class_num =2;                                                 // we have only two classes: ham and spam 
	double class_log_prior[] = {0.0, 0.0};                            //probability for two classes
	double feature_log_prob[][] = new double[class_num][most_common]; // feature parameterized probability
	int SPAM = 1;                                                     //class label
	int HAM = 0;                                                      //class label
	//mean and standard deviation for Gaussian distribution
	double[][] mean = new double[class_num][most_common];
	double[][] std = new double[class_num][most_common];
	
	/**
	 * avoid 0 terms in features
	 */
	double smooth_alpha = 1.0;
	/**
	 * read the file set
	 * @param path
	 */
	public File[] read_file(String path, String process){
		File file = new File(path);
    	if(file.exists()){
    		System.out.println("# of "+process+" files : " + file.list().length);
    	}else{
    		System.out.println("no files");
    	}
    	return file.listFiles();
	}
	
	/**
	 * readin the content of single file
	 * @param file
	 * @return
	 */
	public String readFile(File file) {
		StringBuilder sb = null;
		try {
			InputStream is = new FileInputStream(file);
			BufferedReader buf = new BufferedReader(new InputStreamReader(is));
			String line = buf.readLine();
			line = buf.readLine();
			line = buf.readLine();
			sb = new StringBuilder();

			while (line != null) {
				sb.append(line);
				line = buf.readLine();
			}
			buf.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		return sb == null ? "" : sb.toString();
	}
	
	/**
	 * count the words in total files
	 * @param words
	 */
	public void count_Total_Word(String [] words){
		  for(String s:words){
			  if(!Character.isLetter(s.toCharArray()[0])) {
			      continue;
			  }
		      if(!wordMap.containsKey(s)){  // first time we've seen this string
		          wordMap.put(s, 1);
		      }else{
		          int count = wordMap.get(s);
		          wordMap.put(s, count + 1);
		    }
		  }
	}
	
	/**
	 * count the words in one file
	 * @param words
	 * @param singleWordMap
	 */
	public void count_Word(String[] words, Map<String, Integer> singleWordMap){
		for(String s:words){
			  if(!Character.isLetter(s.toCharArray()[0])) {
			      continue;
			  }
		      if(!singleWordMap.containsKey(s)){  // first time we've seen this string
		    	  singleWordMap.put(s, 1);
		      }else{
		          int count = singleWordMap.get(s);
		          singleWordMap.put(s, count + 1);
		    }
		  }
	}
	/**
	 * find the most common words in files
	 * store in commonMap
	 */
	public void most_common(){
		//sort the hashmap
		// Create a list from elements of HashMap 
        List<Entry<String, Integer> > list = new LinkedList<Map.Entry<String, Integer> >(wordMap.entrySet());
		 Collections.sort(list, new Comparator<Entry<String, Integer>>() {
	            @Override
	            public int compare(Entry<String, Integer> a1, Entry<String, Integer> a2) {
	            	return (a2.getValue()).compareTo(a1.getValue());
	            }
	        });
		//set the value for the most common words
		for(int i=0; i<most_common ; i++){
			commonMap.add(list.get(i).getKey());
		}
	}
	
	/**
	 * generate features according to commonMap
	 * the feature size is determined by most_common
	 * @param features
	 * @param files
	 */
	public void generate_feature(int [][] features, File[] files){
		Map<String, Integer> singleWordMap = new HashMap<String, Integer>();
		
		for(int i = 0 ; i< files.length ; i++){
			singleWordMap.clear();
			String content = readFile(files[i]);
			content.replaceAll("\n", "");
			String [] contents = content.split(" ");
			count_Word(contents, singleWordMap);
			
			for(Entry<String, Integer> entry : singleWordMap.entrySet()){
				if(commonMap.contains(entry.getKey())){
					features[i][commonMap.indexOf(entry.getKey())] = entry.getValue();
				}
			}
		}
	}
	/**
	 * multinomial naive bayes
	 * @param features
	 * @param labels
	 */
	public void MultinomialNB(int[][] features, int[] labels){
		//calculate class_log_prior
		/**
		 * loop over labels
		 * if the value of the term in labels = 1 then ham++ 
		 * if the value of the term in labels = 0 then spam++
		 * class_log_prior[0] = Math.log(ham)
		 * class_log_prior[1] = Math.log(spam)
		 */
		int hamLabels = 0;
		int spamLabels = 0;

		for (int label:
			 labels) {
			if(label == 0)
				spamLabels++;
			else
				hamLabels++;

		}

		class_log_prior[0] = Math.log(hamLabels);
		class_log_prior[1] = Math.log(spamLabels);

		//calculate feature_log_prob
		/**
		 * nested loop over features
		 * for row = features.length
		 *     for col = most_common
		 *         ham[col] + features[row][col]
		 *         spam[col] + features[row][col]
		 *         sum of ham
		 *         sum of spam
		 * for i = most_common
		 *     ham[i] + smooth_alpha
		 *     spam[i] + smooth_alpha
		 * sum of ham += most_common*smooth_alpha
		 * sum of spam += most_common*smooth_alpha
		 * for j = most_common
		 *     feature_log_prob[0] = Math.log(ham[i]/sum of ham)
		 *     feature_log_prob[1] = Math.log(spam[i]/sum of spam)
		 */

		double[] ham = new double[most_common];
		double[] spam = new double[most_common];

		double hamSum = 0;
		double spamSum = 0;


		for (int row = 0; row < features.length; row++)
		{
			for (int col = 0; col < most_common; col++)
			{
				if(labels[row] == 1)
				{
					ham[col] += features[row][col];
					hamSum += features[row][col];
				}
				else
				{
					spam[col] += features[row][col];
					spamSum += features[row][col];
				}
			}
		}

		for (int i = 0; i < most_common; i++)
		{
			ham[i] += smooth_alpha;
			spam[i] += smooth_alpha;
		}

		hamSum += most_common*smooth_alpha;
		spamSum += most_common*smooth_alpha;

		for (int j = 0; j < most_common; j++)
		{
			feature_log_prob[0][j] = Math.log(ham[j]/hamSum);
			feature_log_prob[1][j] = Math.log(spam[j]/spamSum);
		}
	}
	
	/**
	 * Multinomial Naive Bayes prediction
	 * @param features
	 * @return
	 */
	public int[] MultinomialNB_predict(int[][] features){
		int[] classes = new int[features.length];
		/**
		 * nested loop over features with i and j
		 * calculate ham_prob and spam_prob
		 * add ham_prob and spam_prob with class_log_prior
		 * if ham_prob > spam_prob
		 * HAM
		 * else SPAM
		 * return int[] classes
		 */

		for(int i = 0; i < features.length; i++)
		{
			double spamProb = 0;
			double hamProb = 0;

			for (int j = 0; j < features[j].length; j++)
			{
				hamProb	 += features[i][j] * feature_log_prob[0][j];
				spamProb += features[i][j] * feature_log_prob[1][j];
			}
			hamProb += class_log_prior[0];
			spamProb += class_log_prior[1];
			int x;
			if(i == 130)
				x = 0;
			if (Math.abs(spamProb) > Math.abs(hamProb))
				classes[i] = SPAM;
			else
				classes[i] = HAM;
		}
		return classes;
	}
	
	/**
	 * Bernoulli Naive Bayes
	 * @param features
	 * @param labels
	 */
	public void BernoulliNB(int[][] features, int[] labels){
		//convert features to l0-norm
		/**
		 * loop over features with i and j
		 * features[i][j] > 0 ? 1 : 0;
		 */
		//calculate class_log_prior
		/**
		 * loop over labels
		 * if the value of the term in labels = 1 then ham++ 
		 * if the value of the term in labels = 0 then spam++
		 * class_log_prior[0] = Math.log(ham)
		 * class_log_prior[1] = Math.log(spam)
		 */
		//calculate feature_log_prob
		/**
		 * nested loop over features
		 * for row = features.length
		 *     for col = most_common
		 *         ham[col] + features[row][col]
		 *         spam[col] + features[row][col]
		 * for i = most_common
		 *     ham[i] + smooth_alpha
		 *     spam[i] + smooth_alpha
		 * sum of ham = files in ham + smooth_alpha*2 //difference between Multinomial and Bernoulli
		 * sum of spam = files in spam + smooth_alpha*2 //difference between Multinomial and Bernoulli
		 * for j = most_common
		 *     feature_log_prob[0] = ham[i]/sum of ham //no log here
		 *     feature_log_prob[1] = spam[i]/sum of spam //no log here
		 */
	}
	
	/**
	 * Bernoulli Naive Bayes prediction
	 * @param features
	 * @return
	 */
	public int[] BernoulliNB_predict(int[][] features){
		//convert features to l0-norm
		/**
		 * loop over features with i and j
		 * features[i][j] > 0 ? 1 : 0;
		 */

		int[] classes = new int[features.length];
		/**
		 * nested loop over features with i and j
		 * calculate ham_prob and spam_prob
		 *     Math.log(feature_log_prob)*(double)features[i][j] +
		 *         Math.log(1-feature_log_prob)*Math.abs(1-features[i][j])
		 * add ham_prob and spam_prob with class_log_prior
		 * if ham_prob > spam_prob
		 * HAM
		 * else SPAM
		 * return int[] classes
		 */


		for(int i = 0; i < features.length; i++)
		{
			double spamProb = 0;
			double hamProb = 0;

			for (int j = 0; j < features[i].length; j++)
			{

				hamProb	 += features[i][j] * features[1][j];
				spamProb += features[i][j] * features[1][j];
			}
			hamProb += class_log_prior[0];
			spamProb += class_log_prior[1];
			if (Math.abs(spamProb) > Math.abs(hamProb))
				classes[i] = SPAM;
			else
				classes[i] = HAM;
		}
		return classes;

	}
	
	public void GaussianNB(int[][] features, int[] labels){
		
		//calculate mean
		/**
		 * for i in most_common
		 *     for j in features.length
		 *         sum_ham +=features[j][i];
		 *         sum_spam +=features[j][i];
		 *     mean[0] = sum_ham / sum of ham files in labels
		 *     mean[1] = sum_spam / sum of spam files in labels
		 */
		//calculate standard deviation
		/**
		 * for i in most_common
		 *     for j in features.length
		 *         seq_ham +=Math.pow(features[j][i]-mean[0][i], 2);
		 *         seq_spam +=Math.pow(features[j][i]-mean[1][i], 2);
		 *      std[0] = Math.sqrt(seq_ham/sum of ham files in labels);
		 *      std[1] = Math.sqrt(seq_spam/sum of spam files in labels);
		 */
	
	}
	
	/**
	 * 
	 * @param features
	 */
	public int[] GaussianNB_predict(int[][] features){
		
		int[] classes = new int[features.length];
		
		//calculate the Gaussian value for each feature and summ over one specific file
		/**
		 * nested loop over features with i and j
		 * calculate ham_prob and spam_prob
		 *     1.0/(std*Math.sqrt(2.0*Math.PI))*
						Math.exp(-(Math.pow((features[i][j]-mean), 2)/2.0*Math.pow(std, 2)));
		 * if ham_prob > spam_prob
		 * HAM
		 * else SPAM
		 * return int[] classes
		 */
		return classes;
	}
	
	public static void main(String args[]){
		String train_path = "train-mails";
		String test_path = "test-mails";
		email_filter ef = new email_filter();
		
		//construct dictionary
		File[] files = ef.read_file(train_path, "training");
		
		for(int i = 0 ; i< files.length ; i++){
			String content = ef.readFile(files[i]);
			content.replaceAll("\n", "");
			String [] contents = content.split(" ");
			ef.count_Total_Word(contents);
		}
		System.out.println("The maximum of most_common can be: "+ef.wordMap.size());
		//reduce the dictionary size
		//find the most common words in wordmap
		
		ef.most_common();
		
		/**
		 * Multinomial Naive Bayes start
		 */
		//construct model
		//training feature matrix
		int [][] train_features = new int[files.length][commonMap.size()];
		ef.generate_feature(train_features, files);
		
		//copy features for Gaussian as the features will be changed in BernoulliNB
		//and BernoulliNB_predict
		int [][] g_train_features = new int[files.length][commonMap.size()];

		for(int row = 0; row< files.length ; row++){
			for(int col = 0 ; col<commonMap.size(); col++){
				g_train_features[row][col] = train_features[row][col];
			}
		}
		//training labels
		int [] train_labels = new int[files.length];
		Arrays.fill(train_labels, files.length/2, files.length, 1);
		//train model
		ef.MultinomialNB(train_features, train_labels);
		
		//verify model
		//load test data
		files = ef.read_file(test_path, "testing");
		
		//testing feature matrix
		int [][] test_features = new int[files.length][commonMap.size()];
		ef.generate_feature(test_features, files);
		
		//copy features for Gaussian as the features will be changed in BernoulliNB
		//and BernoulliNB_predict
		int [][] g_test_features = new int[files.length][commonMap.size()];
		
		for(int row = 0; row< files.length ; row++){
			for(int col = 0 ; col<commonMap.size(); col++){
				g_test_features[row][col] = test_features[row][col];
			}
		}
		
		//testing labels
		int[] test_labels = new int[files.length];
		Arrays.fill(test_labels, files.length/2, files.length, 1);
		//test model
		int[] classes = ef.MultinomialNB_predict(test_features);
		
		int error = 0;
		for(int i=0 ; i<files.length ; i++){
			if(test_labels[i] == classes[i]){
				error++;
			}
		}
		System.out.println("Multinomial Naive Bayes: "+ (double)error/(double)test_labels.length);
		/**
		 * Multinomial Naive Bayes end
		 */
		
		/**
		 * Bernoulli Naive Bayes start
		 */
		
		ef.BernoulliNB(train_features, train_labels);
		
		classes = ef.BernoulliNB_predict(test_features);
		
		error = 0;
		for(int i=0 ; i<files.length ; i++){
			if(test_labels[i] == classes[i]){
				error++;
			}
		}
		System.out.println("Bernoulli Naive Bayes: "+(double)error/(double)test_labels.length);
		/**
		 * Bernoulli Naive Bayes end
		 */
		
		/**
		 * Gaussian Naive Bayes start
		 */
		//fit the data to Gaussian distribution for each feature of each class
		ef.GaussianNB(g_train_features, train_labels);
		
        classes = ef.GaussianNB_predict(g_test_features);
		
		error = 0;
		for(int i=0 ; i<files.length ; i++){
			if(test_labels[i] == classes[i]){
				error++;
			}
		}
		System.out.println("Gaussian Naive Bayes: "+(double)error/(double)test_labels.length);
		/**
		 * Gaussian Naive Bayes end
		 */
		
	}
}
