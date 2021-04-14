# Processing
All samples were quantified in Salmon using both a PAO1 and PA14 references.

To determine which samples are PAO1 versus PA14 we will use the median expression of accessory genes to determine if a sample is PAO1 or PA14.
In our exploratory analysis we found that samples labeled as PAO1 based on SRA annotations had high PAO1 accessory gene expression.
Whereas samples labeled as PA14 by SRA had high PA14 accessory gene expression.

See plot below where the median expression of PAO1 genes (PAO1 accessory genes) on the x-axis and the median expression of PA14-only genes (PA14 accessory genes) on the y-axis.
Each point is a sample.
![all_samples](https://github.com/greenelab/core-accessory-interactome/blob/master/explore_data/TPM_accessory_genes_all_samples.svg)

A sample is considered PAO1 if the median gene expression of PA14 accessory genes is 0 and PAO1 accessory genes in > 10.
Similarlty, a sample is considered PA14 if the median gene expression of PA14 accessory genes is > 10 and PAO1 accessory genes in 0.

A threshold of 10 is used because we found that using a threshold of 0 included some other SRA-labeled strains.
For example, within the PAO1 binned compendium there are samples that SRA labeled as PAK or Clinical).
![pao1_compendium_0thresdhold](https://github.com/greenelab/core-accessory-interactome/blob/master/processing/TPM_median_acc_expression_pao1_compendium_0threshold.svg)


Similarly for the PA14 compendium.
![pa14_compendium_0thresdhold](https://github.com/greenelab/core-accessory-interactome/blob/master/processing/TPM_median_acc_expression_pa14_compendium_0threshold.svg)

Looking at the distribution of the median accessory gene expression for these non-PAO1 SRA labeled samples (i.e. PAK, Clinical) their expression is very low (blue) compared to all other PAO1 labeled strains (grey).

![pao1_dist_0thresdhold](https://github.com/greenelab/core-accessory-interactome/blob/master/processing/dist_median_acc_expression_pao1_compendium_0threshold.svg)

![pa14_dist_0thresdhold](https://github.com/greenelab/core-accessory-interactome/blob/master/processing/dist_median_acc_expression_pa14_compendium_0threshold.svg)

Using a threshold of 10 we get the following plots that correspond to our final compendia that we will use in our analysis.
As a check, our PAO1 compendium contains ~800 samples and the PA14 compendium contains ~500 samples.
These numbers are close to the numbers that SRA annotates as PAO1 and PA14, ~800 and ~500 respectively.

![pao1_compendium_10thresdhold](https://github.com/greenelab/core-accessory-interactome/blob/master/processing/TPM_median_acc_expression_pao1_compendium_10threshold.svg)

![pa14_compendium_10thresdhold](https://github.com/greenelab/core-accessory-interactome/blob/master/processing/TPM_median_acc_expression_pa14_compendium_10threshold.svg)

![pao1_dist_10thresdhold](https://github.com/greenelab/core-accessory-interactome/blob/master/processing/dist_median_acc_expression_pao1_compendium_10threshold.svg)

![pa14_dist_10thresdhold](https://github.com/greenelab/core-accessory-interactome/blob/master/processing/dist_median_acc_expression_pa14_compendium_10threshold.svg)