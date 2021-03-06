# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1+dev
#   kernelspec:
#     display_name: Python [conda env:core_acc] *
#     language: python
#     name: conda-env-core_acc-py
# ---

# # Align and quantify samples
#
# The second step is to align our samples against our built index and quantify reads. This notebook aligns a pilot set of samples against the PAO1, PA14 and and PAO1 reference genomes.
#
# **Input:**
# * Index of reference transcriptome
# * FASTQ of experimental samples
#
# **Output:**
# * For each query (fragment), the reference sequences (transcripts), strand and position from which the query may have likely originated. In many cases, this mapping information is sufficient for downstream analysis like transcript quantification
# * Each sample will have a quantification file (called quant.sf). The TSV file will contain the name (Name) of each transcript, its length (Length), effective length (EffectiveLength), and its abundance in terms of Transcripts Per Million (TPM) and estimated number of reads (NumReads) originating from this transcript.
#   * The first two columns are self-explanatory, the name of the transcript and the length of the transcript in base pairs (bp).
#   * The effective length represents the various factors that effect the length of transcript (i.e degradation, technical limitations of the sequencing platform)
#   * Salmon outputs ‘pseudocounts’ which predict the relative abundance of different isoforms in the form of three possible metrics (KPKM, RPKM, and TPM). TPM (transcripts per million) is a commonly used normalization method as described in [1] and is computed based on the effective length of the transcript.
#   * Estimated number of reads (an estimate of the number of reads drawn from this transcript given the transcript’s relative abundance and length)
#
# **Algorithm:**
# * Given the index and a set of sequenced reads, the quant command quasi-maps the reads and uses the resulting mapping information to estimate transcript abundances.
# * Quasi-map is a way to map sequenced fragments (single or paired-end reads) to a target transcriptome. Quasi-mapping produces what we refer to as fragment mapping information. In particular, it provides, for each query (fragment), the reference sequences (transcripts), strand and position from which the query may have likely originated. In many cases, this mapping information is sufficient for downstream analysis like quantification.
#
# Basic steps:
# 1. Scan read until k-mer appears in the hash table
# 2. Look up all SA intervals (reference suffixes) containing that k-mer
# 3. Maximum mappable prefix (MMP) finds the longest read sequence that exactly matches the reference suffix
# 4. Determine the next informative position (NIP) by a k-mer skipping approach
# 5. Repeat until the end of the read
# 6. Reports all MMPs that read intersected with
#
# https://hbctraining.github.io/Intro-to-rnaseq-hpc-O2/lessons/08_salmon.html
#
# **Command:**
#
# Command and parameters:
#
# `> ./bin/salmon quant -i transcripts_index -l <LIBTYPE> -1 reads1.fq -2 reads2.fq --validateMappings -o transcripts_quant`
#
# * libtype = Determines how the reads should be interpreted including the relative orientation of paired ends (inward, outward, matching) and strandedness (stranded=specify if read1 comes from forward or reverse strand, unstranded). Currently using “A” which lets Salmon automatically decide
#   * https://salmon.readthedocs.io/en/latest/salmon.html
#   * (pg 38) https://buildmedia.readthedocs.org/media/pdf/salmon/stable/salmon.pdf
# * What does strand bias in output mean? Strand_bias is such that a value of 0.5 means there is no bias (i.e. half of the fragments start with read 1 on the forward strand and half start with read 1 on the reverse complement strand).
#   * Based on lib_format_counts.json file, the bias is very close to 0.5, just above
#   * https://hbctraining.github.io/Intro-to-rnaseq-hpc-O2/lessons/08_salmon.html
#
#

# +
# %load_ext autoreload
# %autoreload 2

import os
import shutil
import pandas as pd
import numpy as np
from core_acc_modules import paths

np.random.seed(123)
# -

# ### Quantify gene expression
# Now that we have our index built and all of our data downloaded, we’re ready to quantify our samples
#
# **For each sample we have read counts per gene (where the genes are based on the reference gene file provided above).**
#
# Note about TPM calculation:
# * For sample A, transcript X will have read count
# * Reads per kilobase (RPK) = read count/length of the transcript
# * Per million scaling factor = sum(read count/length across all samples for that transcript)/1M
# * TPM = RPK/per million scaling factor
# * TPM will depend on the scaling factor. If the number of mapped reads is very low then scale factor will be very low and so any trancript that mapped will be increased to create outliers since we’re dividing by a small scale factor
#
# **How are paired-end vs single-end read samples treated?**
# * The multiple files are treated as a single library, meaning?? In this case we are not specifying
#
# How are we reading the fastq files to be quantified? Are we reading in all files if multipler are provided?

# #### Get quants using PAO1 and phage reference

os.makedirs(paths.PAO1_PHAGE_QUANT, exist_ok=True)

# + magic_args="-s $paths.PAO1_PHAGE_QUANT $paths.FASTQ_DIR $paths.PAO1_PHAGE_INDEX" language="bash"
#
# for FILE_PATH in $2/*;
# do
#
# # get file name
# sample_name=`basename ${FILE_PATH}`
#
# # remove extension from file name
# sample_name="${sample_name%_*}"
#
# # get base path
# base_name=${FILE_PATH%/*}
#
# echo "Processing sample ${base_name}/${sample_name}/*"
#
# salmon quant -i $3 \
#              -l A \
#              -r ${base_name}/${sample_name}/* \
#              -o $1/${sample_name}_quant
# done
# -

# #### Get quants using PA14 and phage reference

os.makedirs(paths.PA14_PHAGE_QUANT, exist_ok=True)

# + magic_args="-s $paths.PA14_PHAGE_QUANT $paths.FASTQ_DIR $paths.PA14_PHAGE_INDEX" language="bash"
#
# for FILE_PATH in $2/*;
# do
#
# # get file name
# sample_name=`basename ${FILE_PATH}`
#
# # remove extension from file name
# sample_name="${sample_name%_*}"
#
# # get base path
# base_name=${FILE_PATH%/*}
#
# echo "Processing sample ${base_name}/${sample_name}/*"
#
# salmon quant -i $3 \
#              -l A \
#              -r ${base_name}/${sample_name}/* \
#              -o $1/${sample_name}_quant
# done
# -

# ### Consolidate sample quantification to gene expression dataframe

# +
# Read through all sample subdirectories in quant/
# Within each sample subdirectory, get quant.sf file
data_dir = paths.PAO1_PHAGE_QUANT

expression_pao1_phage_df = pd.DataFrame(
    pd.read_csv(file, sep="\t", index_col=0)["TPM"].rename(
        file.parent.name.split("_")[0]
    )
    for file in data_dir.rglob("*/quant.sf")
)

expression_pao1_phage_df.head()

# +
# Read through all sample subdirectories in quant/
# Within each sample subdirectory, get quant.sf file
data_dir = paths.PA14_PHAGE_QUANT

expression_pa14_phage_df = pd.DataFrame(
    pd.read_csv(file, sep="\t", index_col=0)["TPM"].rename(
        file.parent.name.split("_")[0]
    )
    for file in data_dir.rglob("*/quant.sf")
)

expression_pa14_phage_df.head()
# -

# Save gene expression data
expression_pao1_phage_df.to_csv(paths.PAO1_PHAGE_GE, sep="\t")
expression_pa14_phage_df.to_csv(paths.PA14_PHAGE_GE, sep="\t")

# **Notes:**
# * Mapping_rate is as expected using PAO1-phage index: _E. coli_ sample had <1%, PAO1 had the largest (~52%) and PA14 had ~32%
# * Mapping_rate for PA14-phage index was <1% for _E. coli_ sample, but had largest mapping for PAO1 (~ 52%) instead of PA14 (~ 30%) sample --> How can i explain this? Checks in the [previous notebook](0_create_reference_genomes.ipynb) that created the input fasta files appears to correctly map PAO1 and PA14. So there isn't an issue where the PAO1 sequences are in a file that we're calling "PA14" for instance. Is this becuase the genome of PA14 is larger?
#
