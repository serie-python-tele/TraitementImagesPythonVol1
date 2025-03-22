import marimo

__generated_with = "0.11.25"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        jupyter: python3
        from: markdown+emoji
        execute:
          echo: true
          eval: true
          message: false
          warning: false
        ---
        """
    )
    return


@app.cell
def _():
    #| echo: false
    #| output: false
    import matplotlib.pyplot as plt
    plt.rcParams['axes.titlesize'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['image.aspect'] = 'equal'
    plt.rcParams['image.cmap'] = 'gray'
    plt.rcParams['figure.dpi'] = 100
    import warnings
    warnings.filterwarnings('ignore')
    return plt, warnings


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Réhaussement et visualisation d'images {#sec-chap02}

        Assurez-vous de lire ce préambule avant d'exécutez le reste du notebook.

        ## Préambule

        ### Objectifs

        Dans ce chapitre, nous abordons quelques techniques de réhaussement et de visualisation d'images. Ce chapitre est aussi disponible sous la forme d'un notebook Python:

        [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/02-RehaussementVisualisationImages.ipynb)

        ::::: bloc_objectif
        :::: bloc_objectif-header
        ::: bloc_objectif-icon
        :::

        **Objectifs d'apprentissage visés dans ce chapitre**
        ::::

        À la fin de ce chapitre, vous devriez être en mesure de :

        -   exploiter les statistiques d'une image pour améliorer la visualisation;
        -   calculer les histogrammes de valeurs;
        -   appliquer une transformation linéaire ou non linéaire pour améliorer une visualisation;
        -   comprendre le principe des composés colorés;
        :::::

        ### 

        ### Bibliothèques

        Les bibliothèques qui vont être explorées dans ce chapitre sont les suivantes:

        -   [SciPy](https://scipy.org/)

        -   [NumPy](https://numpy.org/)

        -   [opencv-python · PyPI](https://pypi.org/project/opencv-python/)

        -   [scikit-image](https://scikit-image.org/)

        -   [Rasterio](https://rasterio.readthedocs.io/en/stable/)

        -   [Xarray](https://docs.xarray.dev/en/stable/)

        -   [rioxarray](https://corteva.github.io/rioxarray/stable/index.html)

        Dans l'environnement Google Colab, seul `rioxarray` et GDAL doivent être installés:
        """
    )
    return


app._unparsable_cell(
    r"""
    #| eval: false
    # magic command not supported in marimo; please file an issue to add support
    # %capture 
    !apt-get update
    !apt-get install gdal-bin libgdal-dev
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Dans l'environnement [Google Colab](https://colab.research.google.com/), il convient de s'assurer que les librairies sont installées:
        """
    )
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %%capture
    # !pip install -qU matplotlib rioxarray xrscipy scikit-image
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Vérifier les importations:
        """
    )
    return


@app.cell
def _():
    import numpy as np
    import rioxarray as rxr
    from scipy import signal
    import xarray as xr
    import xrscipy
    return np, rxr, signal, xr, xrscipy


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Données

        Nous utiliserons les images suivantes dans ce chapitre:
        """
    )
    return


@app.cell
def _():
    #| eval: false
    # magic command not supported in marimo; please file an issue to add support
    # %capture 
    import gdown

    gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a6Ypg0g1Oy4AJt9XWKWfnR12NW1XhNg_', output= 'RGBNIR_of_S2A.tif')
    gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a6O3L_abOfU7h94K22At8qtBuLMGErwo', output= 'sentinel2.tif')
    gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1_zwCLN-x7XJcNHJCH6Z8upEdUXtVtvs1', output= 'berkeley.jpg')
    gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1dM6IVqjba6GHwTLmI7CpX8GP2z5txUq6', output= 'SAR.tif')
    return (gdown,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Vérifiez que vous êtes capable de les lire :
        """
    )
    return


@app.cell
def _(rxr):
    #| output: false

    with rxr.open_rasterio('berkeley.jpg', mask_and_scale= True) as img_rgb:
        print(img_rgb)
    with rxr.open_rasterio('sentinel2.tif', mask_and_scale= True) as img_s2:
        print(img_s2)
    with rxr.open_rasterio('RGBNIR_of_S2A.tif', mask_and_scale= True) as img_rgbnir:
        print(img_rgbnir)
    with rxr.open_rasterio('SAR.tif', mask_and_scale= True) as img_SAR:
        print(img_SAR)
    return img_SAR, img_rgb, img_rgbnir, img_s2


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Visualisation en Python

        ID'emblée, il faut mentionner que Python n'est pas vraiment fait pour visualiser de la donnée de grande taille, le niveau d'interactivité est aussi assez limité. Pour une visualisation interactives, il est plutôt conseillé d'utiliser un outil comme [QGIS](https://qgis.org/). Néanmoins, il est possible de visualiser de petites images avec la librairie [`matplotlib`](https://matplotlib.org/stable/) qui est la librairie principale de visualisation en Python. Cette librairie est extrêmement riche et versatile, nous ne présenterons que les bases nécessaires pour démarrer. Le lecteur désirant aller plus loin pourra consulter les nombreux tutoriels disponibles comme [celui-ci](https://matplotlib.org/stable/tutorials/index.html).

        La fonction de base pour créer une figure est `subplots`, la largeur et la hauteur en pouces de la figure peuvent être contrôlées via le paramètre `figsize`:
        """
    )
    return


@app.cell
def _(plt):
    fig, ax= plt.subplots(figsize=(5, 4))
    plt.show()
    return ax, fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Pour l'affichage des images, la fonction `imshow` permet d'afficher une matrice 2D à une dimension en format *float* ou une matrice RVB avec 3 bandes. Il est important que les dimensions de la matrice soient dans l'ordre hauteur, largeur et bande.
        """
    )
    return


@app.cell
def _(img_rgbnir, plt):
    (fig_1, ax_1) = plt.subplots(figsize=(6, 5))
    plt.imshow(img_rgbnir[0].data)
    plt.show()
    return ax_1, fig_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Pour un affichage à trois bandes, les valeurs seront ramenées sur une échelle de 0 à 1, il est donc nécessaire de normaliser les valeurs avant l'affichage:
        """
    )
    return


@app.cell
def _(img_rgbnir, plt):
    (fig_2, ax_2) = plt.subplots(figsize=(6, 5))
    plt.imshow(img_rgbnir.data.transpose(1, 2, 0) / 2500.0)
    plt.show()
    return ax_2, fig_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        On remarquera les valeurs des axes `x` et `y` avec une origine en haut à gauche. Ceci est un référentiel purement matriciel (lignes et colonnes); autrement dit, il n'y a pas ici de géoréférence. Pour pallier à cette limitation, les librairies `rasterio` et `xarray` proposent une extension de la fonction `imshow` permettant d'afficher les coordonnées cartographiques ainsi qu'un contrôle la dynamique de l'image:
        """
    )
    return


@app.cell
def _(img_rgbnir, plt):
    (fig_3, ax_3) = plt.subplots(figsize=(6, 5))
    img_rgbnir.sel(band=[1, 2, 3]).plot.imshow(vmin=86, vmax=5000)
    ax_3.set_title('Imshow avec rioxarray')
    plt.show()
    return ax_3, fig_3


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ```{=html}
        <!--
        ### Visualisation sur le Web

        Une des meilleures pratiques pour visualiser une image de grande taille est d'utiliser un service de type Web Mapping Service (WMS). Cependant, type de service nécessite une architecture client-serveur qui est plus complexe à mettre en place.

        Google Earth Engine offre des moyens de visualiser de la donnée locale:
        _Working with Local Geospatial Data_ — via [17. Geemap — Introduction to GIS Programming](https://geog-312.gishub.org/book/geospatial/geemap.html#working-with-local-geospatial-data)

        via [data/raster at main · opengeos/data](https://github.com/opengeos/data/tree/main/raster)



        ### Visualisation 3D

        drapper une image satellite sur un DEM


        ## Exercices de révision 
        -->
        ```

        ## Réhaussements visuels

        Le réhaussement visuel d'une image vise principalement à améliorer la qualité visuelle d'une image en améliorant le contraste, la dynamique ou la texture d'une image. De manière générale, ce réhaussement ne modifie pas la donnée d'origine mais il est appliquée dynamiquement à l'affichage pour des fins d'inspection visuelle. Le réhaussement nécessite généralement une connaissance des caractéristiques statistiques d'une image. Ces statistiques sont ensuite exploitées pour appliquer diverses transformations linéaires ou non linéaires.

        ### Statistiques d'une image

        On peut considérer un ensemble de statistique pour chacune des bandes d'une image:

        -   valeurs minimales et maximales

        -   valeurs moyennes,

        -   Quartiles (1er quartile, médiane et 3ième quartile), quantiles et percentiles.

        -   écart-type, et coefficients d'asymétrie (*skewness*) et d'applatissement (*kurtosis*)

        Ces statistiques doivent être calculées pour chaque bande d'une image multispectrale.

        En ligne de commande, `gdalinfo` permet d'interroger rapidement un fichier image pour connaitre ces statistiques univariées de base:
        """
    )
    return


app._unparsable_cell(
    r"""
    !gdalinfo -stats landsat7.tif
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Les librairies de base comme `rasterio` et `xarray` produisent facilement un sommaire des statistiques de base avec la fonction [stats](https://rasterio.readthedocs.io/en/stable/api/rasterio.io.html#rasterio.io.BufferedDatasetWriter.stats):
        """
    )
    return


@app.cell
def _():
    #| eval: false

    import rasterio as rio
    with rio.open('landsat7.tif') as src:
        stats= src.stats()
        print(stats)
    return rio, src, stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        La librairie `xarray` donne accès à des fonctionnalités plus sophistiquées comme le calcul des quantiles:
        """
    )
    return


@app.cell
def _():
    import rioxarray as riox
    with riox.open_rasterio('landsat7.tif', masked=True) as src_1:
        print(src_1)
    quantiles = src_1.quantile(dim=['x', 'y'], q=[0.025, 0.25, 0.5, 0.75, 0.975])
    quantiles
    return quantiles, riox, src_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### Calcul de l'histogramme

        Le calcul d'un histogramme pour une image (une bande) permet d'avoir une vue plus détaillée de la répartition des valeurs radiométriques. Le calcul d'un histogramme nécessite minimalement de faire le choix du nombre de barre ( *bins* ou de la largeur ). Un *bin* est un intervalle de valeurs pour lequel on peut calculer le nombre de valeurs observées dans l'image. La fonction de base pour ce type de calcul est la fonction `numpy.histogram()`:
        """
    )
    return


@app.cell
def _(np):
    array = np.random.randint(0,10,100) # 100 valeurs aléatoires entre 0 et 10
    hist, bin_limites = np.histogram(array, density=True)
    print('valeurs :',hist)
    print(';imites :',bin_limites)
    return array, bin_limites, hist


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Le calcul se fait avec 10 intervalles par défaut.
        """
    )
    return


@app.cell
def _(bin_limites, hist, plt):
    (fig_4, ax_4) = plt.subplots(figsize=(5, 4))
    plt.bar(bin_limites[:-1], hist)
    plt.show()
    return ax_4, fig_4


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Pour des besoins de visualisation, le calcul des valeurs extrêmes de l'histogramme peut aussi se faire via les quantiles comme discutés auparavant.

        ##### Visualisation des histogrammes

        La librarie `rasterio` est probablement l'outil le plus simples pour visualiser rapidement des histogrammes sur une image multi-spectrale:
        """
    )
    return


@app.cell
def _(rio):
    from rasterio.plot import show_hist
    with rio.open('RGBNIR_of_S2A.tif') as src_2:
        show_hist(src_2, bins=50, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title='Histogram')
    return show_hist, src_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Réhaussements linéaires

        Le réhaussement linéaire (*linear stretch*) d'une image est la forme la plus simple de réhaussement, elle consiste à  1) optimiser les valeurs des pixels d'une image afin de maximiser la dynamique disponibles à l'affichage, ou 2) à changer le format de stockage des valeurs (de 8 bits à 16 bits):

        $$ \text{nouvelle valeur d'un pixel} = \frac{\text{valeur d'un pixel} - min_0}{max_0 - min_0}\times (max_1 - min_1)+min_1$$ {#eq-rehauss-lin}

        Par cette opération, on passe de la dynamique de départ ($max_0 - min_0$) vers la dynamique cible ($max_1 - min_1$). Bien que cette opération semble triviale, il est important d'être conscient des trois contraintes suivantes:

         1. **Faire attention à la dynamique cible**, ainsi, pour sauvegarder une image en format 8 bit, on utilisera alors $max_1=255$ et $min_1=0$.

        2\. **Préservation de la valeur de no data** : il faut faire attention à la valeur $min_1$ dans le cas d'une valeur présente pour *no_data*. Par exemple, si *no_data=0* alors il faut s'assurer que $min_1>0$.

        3\. **Précision du calcul** : si possible réaliser la division ci-dessus en format *float*

        #### Cas des histogrammes asymétriques

        Dans certains cas, la distribution de valeurs est très asymétrique et présente une longue queue avec des valeurs extrêmes élevées (à droite ou à gauche de l'histogramme). Le cas des images SAR est particulièrement représentatif de ce type de données. En effet, celles-ci peuvent présenter une distribution de valeurs de type exponentiel. Il est alors préférable d'utiliser des [percentiles](https://fr.wikipedia.org/wiki/Centile) au préalable afin d'explorer la forme de l'histogramme et la distribution des valeurs:
        """
    )
    return


@app.cell
def _(img_SAR, np):
    NO_DATA_FLOAT= -999.0
    # on prend tous les pixels de la première bande
    values = img_SAR[0].values.flatten().astype(float)
    # on exclut les valeurs invalides
    values = values[~np.isnan(values)]
    # on exclut le no data
    values = values[values!=NO_DATA_FLOAT]
    # calcul des percentiles
    percentiles_position= (0,0.1,1,2,50,98,99,99.9,100)
    percentiles= dict(zip(percentiles_position, np.percentile(values, percentiles_position)))
    print(percentiles)
    return NO_DATA_FLOAT, percentiles, percentiles_position, values


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        On constate que la valeur médiane (`0.012`) est très faible, ce qui signifie que 50% des valeurs sont inférieures à cette valeur alors que la valeur maximale (`483`) est 10 000 fois plus élevée! Une manière de visualiser cette distribution de valeurs est d'utiliser [`boxplot`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html) et [`violinplot`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.violinplot.html) de la librairie `matplotlib`:
        """
    )
    return


@app.cell
def _(plt, values):
    (fig_5, ax_5) = plt.subplots(nrows=2, ncols=1, figsize=(6, 4), sharex=True)
    ax_5[0].set_title('Distribution de la bande 0 de img_SAR', fontsize='small')
    ax_5[0].grid(True)
    ax_5[0].violinplot(values, orientation='horizontal', quantiles=(0.01, 0.02, 0.5, 0.98, 0.99), showmeans=False, showmedians=True)
    ax_5[1].set_xlabel('Valeur des pixels')
    ax_5[1].grid(True)
    bplot = ax_5[1].boxplot(values, notch=True, orientation='horizontal')
    plt.tight_layout()
    plt.show()
    return ax_5, bplot, fig_5


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Afin de visualiser correctement l'histogramme, il faut se limiter à un intervalle de valeurs plus réduit. Dans le code ci-dessous, on impose à la fonction `np.histogramme` de compter les valeurs de pixels dans des intervalles de valeurs fixés par la fonction `np.linspace(percentiles[0.1],percentiles[99.9], 50)` où `percentiles[0.1]` et `percentiles[99.9]` sont les $0.1\%$ et $99.9\%$ percentiles respectivement:
        """
    )
    return


@app.cell
def _(np, percentiles, plt, values):
    (hist_1, bin_edges) = np.histogram(values, bins=np.linspace(percentiles[0.1], percentiles[99.9], 50), density=True)
    (fig_6, ax_6) = plt.subplots(nrows=2, ncols=1, figsize=(6, 5), sharex=True)
    ax_6[0].bar(bin_edges[:-1], hist_1 * (bin_edges[1] - bin_edges[0]), width=bin_edges[1] - bin_edges[0], edgecolor='w')
    ax_6[0].set_title('Distribution de probabilité (PDF)')
    ax_6[0].set_ylabel('Densité de probabilité')
    ax_6[0].grid(True)
    ax_6[1].plot(bin_edges[:-1], hist_1.cumsum() * (bin_edges[1] - bin_edges[0]))
    ax_6[1].set_title('Distribution de probabilité cumulée (CDF)')
    ax_6[1].set_xlabel('Valeur du pixel')
    ax_6[1].set_ylabel('Probabilité cumulée')
    ax_6[1].grid(True)
    plt.tight_layout()
    plt.show()
    return ax_6, bin_edges, fig_6, hist_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Au niveau de l'affichage avec `matplotlib`, la dynamique peut être contrôlée directement avec les paramètres `vmin` et `vmax` comme ceci:
        """
    )
    return


@app.cell
def _(img_SAR, percentiles, plt):
    (fig_7, ax_7) = plt.subplots(nrows=2, ncols=2, figsize=(6, 5), sharex=True, sharey=True)
    [a.axis('off') for a in ax_7.flatten()]
    ax_7[0, 0].imshow(img_SAR[0].values, vmin=percentiles[0], vmax=percentiles[100])
    ax_7[0, 0].set_title(f'0% - 100%={percentiles[0]:2.1f} - {percentiles[100]:2.1f}')
    ax_7[0, 1].imshow(img_SAR[0].values, vmin=percentiles[0.1], vmax=percentiles[99.9])
    ax_7[0, 1].set_title(f'0.1% - 99.9%={percentiles[0.1]:2.1f} - {percentiles[99.9]:2.1f}')
    ax_7[1, 0].imshow(img_SAR[0].values, vmin=percentiles[1], vmax=percentiles[99])
    ax_7[1, 0].set_title(f'1% - 99%={percentiles[1]:2.1f} - {percentiles[99]:2.1f}')
    ax_7[1, 1].imshow(img_SAR[0].values, vmin=percentiles[2], vmax=percentiles[98])
    ax_7[1, 1].set_title(f'2% - 98%={percentiles[2]:2.1f} - {percentiles[98]:2.1f}')
    plt.tight_layout()
    return ax_7, fig_7


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Réhaussements non linéaires

        #### Réhaussement par fonctions

        ```{=html}
        <!--
        Calcul d'histogrammes, étirement, égalisation, styling
        -->
        ```

        Le réhaussenent par fonction consiste à appliquer une fonction non linéaire afin de modifier la dynamique de l'image. Par exemple, pour une image radar, une transformation populaire est d'afficher les valeurs de rétrodiffusion en décibel (`dB`) avec la fonction `log10()`.
        """
    )
    return


@app.cell
def _(img_SAR, np):
    percentiles_position_1 = (0, 0.1, 1, 2, 50, 98, 99, 99.9, 100)
    values_1 = 10 * np.log10(img_SAR[0]).data
    percentiles_db = dict(zip(percentiles_position_1, np.percentile(values_1, percentiles_position_1)))
    print(percentiles_db)
    return percentiles_db, percentiles_position_1, values_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Les boites à moustache (*boxplots*) ont une bien meilleure distribution qui est en effet très proche d'une distribution normale gaussienne:
        """
    )
    return


@app.cell
def _(plt, values_1):
    (fig_8, ax_8) = plt.subplots(nrows=2, ncols=1, figsize=(6, 4), sharex=True)
    ax_8[0].set_title('Distribution de la bande 0 de img_SAR en dB', fontsize='small')
    ax_8[0].grid(True)
    ax_8[0].violinplot(values_1.flatten(), orientation='horizontal', quantiles=(0.01, 0.02, 0.5, 0.98, 0.99), showmeans=False, showmedians=True, showextrema=True)
    ax_8[1].set_xlabel('Valeur des pixels')
    ax_8[1].grid(True)
    bplot_1 = ax_8[1].boxplot(values_1.flatten(), notch=True, orientation='horizontal')
    plt.tight_layout()
    plt.show()
    return ax_8, bplot_1, fig_8


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        On obtient ainsi les images suivantes:
        """
    )
    return


@app.cell
def _(percentiles_db, plt, values_1):
    (fig_9, ax_9) = plt.subplots(nrows=2, ncols=2, figsize=(6, 5), sharex=True, sharey=True)
    [a.axis('off') for a in ax_9.flatten()]
    ax_9[0, 0].imshow(values_1, vmin=percentiles_db[0], vmax=percentiles_db[100])
    ax_9[0, 0].set_title(f'0% - 100%={percentiles_db[0]:2.1f} - {percentiles_db[100]:2.1f}')
    ax_9[0, 1].imshow(values_1, vmin=percentiles_db[0.1], vmax=percentiles_db[99.9])
    ax_9[0, 1].set_title(f'0.1% - 99.9%={percentiles_db[0.1]:2.1f} - {percentiles_db[99.9]:2.1f}')
    ax_9[1, 0].imshow(values_1, vmin=percentiles_db[1], vmax=percentiles_db[99])
    ax_9[1, 0].set_title(f'1% - 99%={percentiles_db[1]:2.1f} - {percentiles_db[99]:2.1f}')
    ax_9[1, 1].imshow(values_1, vmin=percentiles_db[2], vmax=percentiles_db[98])
    ax_9[1, 1].set_title(f'2% - 98%={percentiles_db[2]:2.1f} - {percentiles_db[98]:2.1f}')
    plt.tight_layout()
    return ax_9, fig_9


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ```{=html}
        <!--
        Exercise: trouver une autre transformation possible pour l'image SAR.
        -->
        ```

        #### Égalisation d'histogramme

        L'égalisation d'histogramme consiste à modifier les valeurs des pixels d'une image source afin que la distribution cumulée des valeurs (CDF) devienne similaire à celle d'une image cible. La CDF (*Cumulative Distribution Function*) est simplement la somme cumulée des valeurs de l'histogramme:

        $$
        CDF_{source}(i)= \frac{1}{K}\sum_{j=0}^{j \leq i} hist_{source}(j)
        $$ avec $K$ choisit de façon à ce que la dernière valeur soit égale à 1 ($CDF_{source}(i_{max})=1$). De la même manière, $CDF_{cible}$ est la CDF d'une image cible. La formule générale pour l'égalisation d'histogramme est la suivante: $$
        j = CDF_{cible}^{-1}(CDF_{source}(i))
        $$

        On peut choisir $CDF_{cible}$ comme correspondant à une image où chaque valeur de pixel est équiprobable (d'où le terme *égalisation*), ce qui veut dire $hist_{cible}(j)=1/L$ avec $L$ égale au nombre de valeurs possibles dans l'image (par exemple $L=256$). $$
        j = L \times CDF_{source}(i)
        $$ On peut appliquer cette procédure sur l'image SAR en dB de la façon suivante:
        """
    )
    return


@app.cell
def _(img_SAR, np, plt):
    values_2 = np.sort(np.log10(img_SAR[0].data.flatten()))
    cdf_x = np.linspace(values_2[0], values_2[-1], 1000)
    cdf_source = np.interp(cdf_x, values_2, np.arange(len(values_2)) / len(values_2) * 255)
    values_eq = np.interp(np.log10(img_SAR[0].data), cdf_x, cdf_source).astype('uint8')
    plt.imshow(values_eq)
    plt.axis('off')
    return cdf_source, cdf_x, values_2, values_eq


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ```{=html}
        <!--
        Exercise: changer la CDF cible pour une Gaussienne
        -->
        ```

        #### Palettes de couleur

        Les palettes de couleurs sont appliquées dynamiquement à l'affichage sur une image à une seule bande. La librairie `matplotlib` contient un nombre considérable de [palettes](https://matplotlib.org/stable/users/explain/colors/colormaps.html).
        """
    )
    return


@app.cell
def _():
    # | output: false
    from matplotlib import colormaps
    list(colormaps)
    return (colormaps,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Voici quelques exemples ci-dessous, les valeurs de l'image doivent être normalisées entre 0 et 1 ou entre 0 et 255 sinon les paramètres `vmin` et `vmax` doivent être spécifiés. On peut observer comment ces palettes révèlent les détails de l'image malgré une image originalement très sombre.
        """
    )
    return


@app.cell
def _(img_SAR, percentiles, plt):
    (fig_10, ax_10) = plt.subplots(nrows=2, ncols=2, figsize=(6, 5), sharex=True, sharey=True)
    [a.axis('off') for a in ax_10.flatten()]
    ax_10[0, 0].imshow(img_SAR[0].data, vmin=percentiles[2], vmax=percentiles[98], cmap='jet')
    ax_10[0, 0].set_title(f'jet')
    ax_10[0, 1].imshow(img_SAR[0].data, vmin=percentiles[2], vmax=percentiles[98], cmap='hot')
    ax_10[0, 1].set_title(f'hot')
    ax_10[1, 0].imshow(img_SAR[0].data, vmin=percentiles[2], vmax=percentiles[98], cmap='hsv')
    ax_10[1, 0].set_title(f'hsv')
    ax_10[1, 1].imshow(img_SAR[0].data, vmin=percentiles[2], vmax=percentiles[98], cmap='terrain')
    ax_10[1, 1].set_title(f'terrain')
    plt.tight_layout()
    return ax_10, fig_10


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Il peut être utile d'ajouter une barre de couleurs afin d'indiquer la correspondance entre les couleurs et les valeurs numériques:
        """
    )
    return


@app.cell
def _(img_SAR, percentiles, plt):
    import matplotlib as mpl
    (fig_11, ax_11) = plt.subplots(figsize=(6, 6))
    cmap = mpl.colormaps.get_cmap('jet').with_extremes(under='white', over='magenta')
    h = plt.imshow(img_SAR[0].data, norm=mpl.colors.LogNorm(vmin=percentiles[2], vmax=percentiles[98]), cmap=cmap)
    fig_11.colorbar(h, ax=ax_11, orientation='horizontal', label='Intensité', extend='both')
    ax_11.axis('off')
    return ax_11, cmap, fig_11, h, mpl


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Composés colorés

        Le système visuel humain est sensible seulement à la partie visible du spectre électromagnétique qui compose les couleurs de l'arc-en-ciel du bleu au rouge. L'ensemble des couleurs du spectre visible peut être obtenu à partir du mélange de trois couleurs primaires (rouge, vert et bleu). Ce système de décomposition à trois couleurs est à la base de la plupart des systèmes de visualisation ou de représentation de l'information de couleur. Si on prend le cas des images Sentinel-2, 12 bandes sont disponibles, plusieurs composés couleurs sont donc possibles (voir le site de [Copernicus](https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/composites/)). Voici quelques exemples possibles, chaque composé mettant en valeur des propriétés différentes de la surface.
        """
    )
    return


@app.cell
def _(img_s2, plt):
    (fig_12, ax_12) = plt.subplots(nrows=2, ncols=2, figsize=(8, 6), sharex=True, sharey=True)
    img_s2.sel(band=[4, 3, 2]).plot.imshow(vmin=86, vmax=4000, ax=ax_12[0, 0])
    ax_12[0, 0].set_title('RVB')
    img_s2.sel(band=[8, 3, 2]).plot.imshow(vmin=86, vmax=4000, ax=ax_12[0, 1])
    ax_12[0, 1].set_title('NIR,V,B')
    img_s2.sel(band=[12, 8, 4]).plot.imshow(vmin=86, vmax=4000, ax=ax_12[1, 0])
    ax_12[1, 0].set_title('SWIR2,NIR,R')
    img_s2.sel(band=[12, 11, 4]).plot.imshow(vmin=86, vmax=4000, ax=ax_12[1, 1])
    ax_12[1, 1].set_title('SWIR2,SWIR1,NIR')
    plt.tight_layout()
    plt.show()
    return ax_12, fig_12


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
