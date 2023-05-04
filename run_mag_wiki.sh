#!/bin/bash
#SBATCH --job-name="mini_wiki_mag"
#SBATCH -D .
#SBATCH --output=./logs/mini_wiki_mag_specter_%j.out
#SBATCH --error=./logs/mini_wiki_mag_specter_%j.err
#SBATCH --ntasks=1
#SBATCH --gres gpu:2
#SBATCH --cpus-per-task=128
#SBATCH --time=2-0:00:00

module load gcc/10.2.0 rocm/4.0.1 mkl/2018.4 intel/2018.4 python/3.7.4 
source ../venv/bin/activate
export LD_LIBRARY_PATH=/gpfs/projects/bsc88/projects/bne/eval_amd/scripts_to_run/external-lib:$LD_LIBRARY_PATH

SEED=123
NUM_EPOCHS=10
BATCH_SIZE=8
GRADIENT_ACC_STEPS=2
LEARN_RATE=0.00005
WARMUP=0.06
WEIGHT_DECAY=0.1
MAX_SEQ_LENGTH=512

MODEL='../models/roberta-large'
DATA_LOADER='./loader_mag_wiki.py'
OUTPUT_DIR='./output'
LOGGING_DIR='./tb'
CACHE_DIR='./.cache'

BATCH_SIZE_PER_GPU=$(( $BATCH_SIZE*$GRADIENT_ACC_STEPS ))
DIR_NAME='mini_wiki_mag'_${BATCH_SIZE_PER_GPU}_${WEIGHT_DECAY}_${LEARN_RATE}_$(date +"%m-%d-%y_%H-%M")

python ./run_glue.py --model_name_or_path $MODEL --seed $SEED \
		     --dataset_name $DATA_LOADER \
		     --task_name mag_wiki --do_train --do_eval --do_predict \
		     --num_train_epochs $NUM_EPOCHS \
		     --gradient_accumulation_steps $GRADIENT_ACC_STEPS \
		     --per_device_train_batch_size $BATCH_SIZE \
		     --max_seq_length $MAX_SEQ_LENGTH \
		     --learning_rate $LEARN_RATE \
		     --weight_decay $WEIGHT_DECAY \
		     --warmup_ratio $WARMUP \
		     --output_dir $OUTPUT_DIR/$DIR_NAME --overwrite_output_dir \
		     --logging_dir $LOGGING_DIR/$DIR_NAME --logging_strategy epoch \
		     --cache_dir $CACHE_DIR/$DIR_NAME --overwrite_cache \
		     --metric_for_best_model accuracy --evaluation_strategy epoch --load_best_model_at_end

# 			 --max_train_samples 20000 --max_eval_samples 5000 --max_predict_samples 5000

