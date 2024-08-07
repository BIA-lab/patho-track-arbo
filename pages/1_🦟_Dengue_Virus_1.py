from config import *
from source.pages import sidebar_dengue_1 as sd
from source.pages.header import *
from source.graphs.africa_map import *
from source.graphs.variants_proportion import variants_bar_plot
from source.graphs.other_countries_sequences import other_countries_with_sequences_chart
from source.pages.sidebar_dengue_1 import choose_colour_dengue_genotype

from source.pages.tables import variant_summary_table as vst


def main():
    st.set_page_config(
        page_title="Dengue Virus 1 Africa Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="img/cropped-ceri_branco-01-150x150.png"
    )

    st.markdown(css_changes, unsafe_allow_html=True)
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    ## Getting the data
    df_africa = load_data('data/dengue/metadata-dengue-1.csv')

    ##### CHECK LAST UPDATE #####
    with open('last_update.txt', 'r') as f:
        last_update = f.readlines()[-1]
    # last_update = datetime.today().strftime("%Y-%m-%d")

    ## Add sidebar to the app
    st.sidebar.title("CLIMADE AFRICA - DENGUE")
    st.sidebar.subheader("Last update: %s" % last_update)

    # Sidebar filter data
    st.sidebar.markdown(" ")
    st.sidebar.header("Filter data ")

    ### Begin of filters

    # Filter data by countries
    countries_choice, display_countries = sd.get_countries_choice(df_africa)

    # Sidebar filter lineages
    lineages_choice = sd.get_lineages_choice(df_africa)

    # Sidebar filter period
    start_date, end_date = sd.get_dates_choice(df_africa)

    ### Auxiliar dataframes ###

    # Couting variants
    df_count_country = sd.new_build_df_count(df_africa, country=True)
    other_df_count_country = sd.other_build_df_count(df_africa, country=True)
    other_df_count = sd.other_build_df_count(df_africa)
    variants_percentage, pivot_df = sd.new_build_variant_percentage(other_df_count)
    

    ### Filter and reset buttons ###
    bt_col_1, bt_col_2 = st.sidebar.columns(2)
    if bt_col_1.button("Reset filters", key='button_reset_filters'):
        sd.reset_filters(df_africa)

    # # Button to call filtering function
    if bt_col_2.button("Filter data", key='button_filter'):
        df_africa = sd.filter_df_africa(countries_choice, lineages_choice, start_date, end_date, df_africa)
        df_count_country = sd.new_build_df_count(df_africa, country=True)
        other_df_count = sd.other_build_df_count(df_africa)
        variants_percentage, pivot_df = sd.new_build_variant_percentage(other_df_count)
        other_df_count_country = sd.other_build_df_count(df_africa, country=True)

    # End of sidebar
    # Metrics
    sd.show_metrics(df_africa)

    # st.sidebar.header("Acknowledgment")
    # sd.acknowledgment_section(logo_path='img/gisaid_logo.png', link='https://www.gisaid.org/')

    # Add title and subtitle to the main interface of the app
    main_title("DENGUE VIRUS 1 - AFRICA DASHBOARD" , display_countries)

    ### Layout of main page
    c1, c2 = st.columns((1.5, 1.9))

    ############ First column ###############
    ############## MAP CHART ################
    c1.subheader("Genomes per country")
    map_option = c1.selectbox(
        'Metric',
        ('Total number of genomes', 'Genomes by genotype'
         # 'Variants proportion'
         ))
    if map_option == 'Total number of genomes':
        colorpath_africa_map(df_count_country, column=c1, color_pallet="sunsetdark")
    elif map_option == 'Genomes by genotype':
        # Multiselect to choose variants to show
        voc_selected = c1.selectbox("Choose genotype to show", dengue_one)
        df_count_map = sd.new_build_df_count(df_africa[df_africa['lineage'] == voc_selected], True)
        colorpath_africa_map(df_count_map, column=c1, color_pallet=dengue_one_color.get(voc_selected))
    # elif map_option == 'Variants proportion':
    #     c1.write(variants_percentage.head())
    #     scatter_africa_map(variants_percentage, column=c1, map_count_column='Count')

    ############ Second column ###############
    ####### Circulating lineages CHART ###########
    variants_bar_plot(variants_percentage, c2, "Circulating Genotypes", pivot_df, choose_colour_dengue_genotype, "Genotype")

    ####### COUNTRIES WHITH SEQUENCE CHART #########
    other_countries_with_sequences_chart(other_df_count_country, c2, discrete_colour_dengue_genotypes, "Genotype")

if __name__ == "__main__":
    main()