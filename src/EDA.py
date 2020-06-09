import logging 
import os
import numpy as np
import yaml
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def EDA(data, fea1, fea2, fea3, fea4, fea5, target):
    """ Perfrom exploratory data analysis
    params:
        data(:py:class:`pandas.DataFrame`): DataFrame containing features and target.
        target (str): Target label. 
    Returns:
        figs: List of plots 
    """
    ## Correlation 
    figs = []
    f, ax = plt.subplots(figsize=(10, 8))
    corr = data.corr()
    sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(240,10,as_cmap=True),
            square=True, ax=ax)
    figs.append(f)

    # Distribution of charges 
    f, ax = plt.subplots(figsize=(10, 8))
    ax.hist(data.charges)
    ax.title.set_text("Distribution of charges")
    ax.set_xlabel("Charges")
    ax.set_ylabel("Count")
    figs.append(f)

    # Distribution of charges for smokers and non-smokers
    f= plt.figure(figsize=(12,5))
    ax=f.add_subplot(121)
    sns.distplot(data[(data[fea1] == 1)][target],color='c',ax=ax)
    ax.set_title('Distribution of charges for smokers')

    ax=f.add_subplot(122)
    sns.distplot(data[(data[fea1] == 0)][target],color='b',ax=ax)
    ax.set_title('Distribution of charges for non-smokers')
    figs.append(f)

    ## Gender
    f = sns.factorplot(x=fea1, kind="count",hue = fea2, palette="pink", data=data)
    figs.append(f)

    # Charges for women 
    f= plt.figure(figsize=(12,5))
    plt.title("Box plot for charges of women")
    sns.boxplot(y=fea1, x=target, data =  data[(data[fea2] == 0)] , orient="h", palette = 'magma')
    figs.append(f)

    # Charges for men
    f = plt.figure(figsize=(12,5))
    plt.title("Box plot for charges of men")
    sns.boxplot(y=fea1, x=target, data =  data[(data[fea2] == 1)] , orient="h", palette = 'rainbow')
    figs.append(f)

    ## Age 
    f = plt.figure(figsize=(12,5))
    plt.title("Distribution of age")
    ax = sns.distplot(data[fea3], color = 'g')
    figs.append(f)

    # Distribution of charges and age for non-smokers
    #non - smokers
    g = sns.jointplot(x=fea3, y=target, data = data[(data[fea1] == 0)],kind="kde", color="c")
    g.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
    g.ax_joint.collections[0].set_alpha(0)
    g.set_axis_labels("$X$", "$Y$")
    ax.set_title('Distribution of charges and age for non-smokers')
    figs.append(g)
    
    # Distribution of charges and age for smokers
    g = sns.jointplot(x="age", y="charges", data = data[(data[fea1] == 1)],kind="kde", color="m")
    g.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
    g.ax_joint.collections[0].set_alpha(0)
    g.set_axis_labels("$X$", "$Y$")
    ax.set_title('Distribution of charges and age for smokers')
    figs.append(g)

    # Smokes vs non smokers
    f = sns.lmplot(x=fea3, y=target, hue=fea1, data=data, palette = 'magma', size = 7)
    ax.set_title('Smokers and non-smokers')
    figs.append(f)

    ## bmi
    f = plt.figure(figsize=(12,5))
    plt.title("Distribution of bmi")
    ax = sns.distplot(data[fea4], color = 'b')

    # Distribution of charges for patients with BMI greater than 30
    f = plt.figure(figsize=(12,5))
    plt.title("Distribution of charges for patients with BMI greater than 30")
    ax = sns.distplot(data[(data[fea4] >= 30)][target], color = 'm')
    figs.append(f)

    # Distribution of charges for patients with BMI less than 30
    f = plt.figure(figsize=(12,5))
    plt.title("Distribution of charges for patients with BMI less than 30")
    ax = sns.distplot(data[(data[fea4] < 30)][target], color = 'b')
    figs.append(f)

    
    # Scatter plot of charges and bmi
    f= plt.figure(figsize=(10,6))
    ax = sns.scatterplot(x=fea4,y=target,data=data,palette='magma',hue=fea1)
    ax.set_title('Scatter plot of charges and bmi')
    figs.append(f)

    l = sns.lmplot(x=fea4, y=target, hue=fea1, data=data, palette = 'magma', size = 8)
    figs.append(l)

    ## Children 
    c = sns.catplot(x=fea5, kind="count", palette="rainbow", data=data, size = 6)
    figs.append(c)
    
    # Smokers and non-smokers who have childrens
    f = sns.catplot(x=fea1, kind="count", palette="magma",hue = fea2,
            data=data[(data[fea5] > 0)], size = 6)
    ax.set_title('Smokers and non-smokers who have childrens')
    figs.append(f)

    return figs

def plotting(args):
    """Run defined functions
    Args:
        parsed argument input
    Returns:
        None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    data = pd.read_csv(args.input1)
    logger.info('Porcessed data loaded from %s', args.input1)
    fig = EDA(data,**config['EDA']['EDA'])

    for i, figure in enumerate(fig):
        figure.savefig(os.path.join(args.output, 'figure%d.png' % i))
    logger.info("Plots saved to %s", args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EDA plots")
    parser.add_argument('--input1', default="data/processed_data.csv", help='Path to input features')
    parser.add_argument('--config', default='config/model_config.yaml',
                        help='path to yaml file with configurations')
    parser.add_argument('--output', default="figures", help='Path to save output plots')
    args = parser.parse_args()

    plotting(args)