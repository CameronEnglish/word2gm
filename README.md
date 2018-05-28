# Word2GM (Word to Gaussian Mixture)

This is an implementation of the model in *[Athiwaratkun and Wilson](https://arxiv.org/abs/1704.08424), Multimodal Word Distributions, ACL 2017* with slight modifications to focus on examining the implications of higher K values, particularly with reference to the problem of acronym word-sense disambiguation.



## Training Data
The data used in the paper is the concatenation of *ukWaC* and *WaCkypedia_EN*, both of which can be requested [here](http://wacky.sslmit.unibo.it/doku.php?id=download).

Additional training on the English language Wikipedia was performed.


## Dependencies
Tensorflow 0.12 (version number important -- Skipgram functionality issue otherwise)

[ggplot](https://github.com/yhat/ggplot.git)
```
pip install -U ggplot
# or 
conda install -c conda-forge ggplot
# or
pip install git+https://github.com/yhat/ggplot.git
```


## Steps
Below are the steps for training and visualization with text8 dataset.
1. Obtain the dataset and train.
```
bash get_text8.sh
python word2gm_trainer.py --num_mixtures 2 --train_data data/text8 --spherical --embedding_size 50 --epochs_to_train 10 --var_scale 0.05 --save_path modelfiles/t8-2s-e10-v05-lr05d-mc100-ss5-nwout-adg-win10 --learning_rate 0.05  --subsample 1e-5 --adagrad  --min_count 5 --batch_size 128 --max_to_keep 100 --checkpoint_interval 500 --window_size 10
# or simply calling ./train_text8.sh
```
See at the end of page for details on training options.

2. Note that the model will be saved at modelfiles/t8-2s-e10-v05-lr05d-mc100-ss5-nwout-adg-win10. The code to analyze the model and visualize the results is in **Analyze Text8 Model.ipynb**. See model API below.


3. We can visualize the word embeddings itself by executing the following command in iPynb:
```
w2gm_text8_2s.visualize_embeddings()
```
This command prepares the word embeddings to be visualized by Tensorflow's Tensorboard. Once the embeddings are prepared, the visualization can be done by shell command:
```
tensorboard --logdir=modelfiles/t8-2s-e10-v05-lr05d-mc100-ss5-nwout-adg-win10_emb --port=6006
```
Then, navigate the browser to (http://localhost/6006) (or a url of the appropriate machine that has the model) and click at the **Embeddings** tab. Note that the **logdir** folder is the "**original-folder**" + "_emb".

## Visualization
The Tensorboard embeddings visualization tools (please use Firefox or Chrome) allow for nearest neighbors query, in addition to PCA and t-sne visualization. We use the following notation: *x:i* refers to the *i*th mixture component of word 'x'. For instance, querying for 'bank:0' yields 'river:1', 'confluence:0', 'waterway:1' as the nearest neighbors, which means that this component of 'bank' corresponds to river bank. On the other hand, querying for 'bank:1' gives the nearest neighbors 'banking:1', 'banker:0', 'ATM:0', which indicates that this component of 'bank' corresponds to financial bank.


We provide visualization (compatible with Chrome and Firefox) for our models trained on *ukWaC+WaCkypedia* for [K=1](http://35.161.153.223:6001), [K=2](http://35.161.153.223:6002), and [K=3](http://35.161.153.223:6003).


## Trained Model
We provide a trained model for K=2 [here](http://35.161.153.223:6004/w2gm-k2-d50.tar.gz). To analyze the model, see **Analyze Model.ipynb**. The code expects the model to be extracted to directory **modelfiles/w2gm-k2-d50/**.


### Training on large datasets
Our code relies on the word sampling implementation of Tensorflow. Existing implementation of Tensorflow can handle a dataset up to a certain size (~4GB) but would throw an error for larger datasets such as *ukWaC+WaCkypedia* (17GB).

To train on a very large dataset, we provide a version of Tensorflow (0.11.0rc1) with a modified SkipGram method that can handle large datasets (https://github.com/benathi/tensorflow_0.11_robust_skipgram). You can build Tensorflow from source using this version. (See instructions for building from source [here](https://www.tensorflow.org/versions/r0.11/get_started/os_setup#installing_from_sources).) Large datasets also require large RAM since we load the entire dataset into memory. For *ukWaC+WaCkypedia*, a required RAM is about 32GB+.



 ## Training Options
 
 ```
 arguments:
   -h, --help            show this help message and exit
   --save_path SAVE_PATH
                         Directory to write the model and training summaries.
                         (required)
   --train_data TRAIN_DATA
                         Training text file. (required)
   --embedding_size EMBEDDING_SIZE
                         The embedding dimension size.
   --epochs_to_train EPOCHS_TO_TRAIN
                         Number of epochs to train. Each epoch processes the
                         training data once completely.
   --learning_rate LEARNING_RATE
                         Initial learning rate.
   --batch_size BATCH_SIZE
                         Number of training examples processed per step (size
                         of a minibatch).
   --concurrent_steps CONCURRENT_STEPS
                         The number of concurrent training steps.
   --window_size WINDOW_SIZE
                         The number of words to predict to the left and right
                         of the target word.
   --min_count MIN_COUNT
                         The minimum number of word occurrences for it to be
                         included in the vocabulary.
   --subsample SUBSAMPLE
                         Subsample threshold for word occurrence. Words that
                         appear with higher frequency will be randomly down-
                         sampled. Set to 0 to disable.
   --statistics_interval STATISTICS_INTERVAL
                         Print statistics every n seconds.
   --summary_interval SUMMARY_INTERVAL
                         Save training summary to file every n seconds (rounded
                         up to statistics interval).
   --checkpoint_interval CHECKPOINT_INTERVAL
                         Checkpoint the model (i.e. save the parameters) every
                         n seconds (rounded up to statistics interval).
   --num_mixtures NUM_MIXTURES
                         Number of mixture component for Mixture of Gaussians
   --spherical [SPHERICAL]
                         Whether the model should be spherical of diagonalThe
                         default is spherical
   --nospherical
   --var_scale VAR_SCALE
                         Variance scale
   --ckpt_all [CKPT_ALL]
                         Keep all checkpoints(Warning: This requires a large
                         amount of disk space).
   --nockpt_all
   --norm_cap NORM_CAP   The upper bound of norm of mean vector
   --lower_sig LOWER_SIG
                         The lower bound for sigma element-wise
   --upper_sig UPPER_SIG
                         The upper bound for sigma element-wise
   --mu_scale MU_SCALE   The average norm will be around mu_scale
   --objective_threshold OBJECTIVE_THRESHOLD
                         The threshold for the objective
   --adagrad [ADAGRAD]   Use Adagrad optimizer instead
   --noadagrad
   --loss_epsilon LOSS_EPSILON
                         epsilon parameter for loss function
   --constant_lr [CONSTANT_LR]
                         Use constant learning rate
   --noconstant_lr
   --wout [WOUT]         Whether we would use a separate wout
   --nowout
   --max_pe [MAX_PE]     Using maximum of partial energy instead of the sum
   --nomax_pe
   --max_to_keep MAX_TO_KEEP
                         The maximum number of checkpoint files to keep
   --normclip [NORMCLIP]
                         Whether to perform norm clipping (very slow)
   --nonormclip
 
 ```
