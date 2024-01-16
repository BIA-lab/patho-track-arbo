from config import *
from source.pages import sidebar_dengue_all_serotypes as sd
from source.pages.header import *
from source.graphs.africa_map import *
from source.graphs.variants_proportion import variants_bar_plot
from source.graphs.countries_sequences import countries_with_sequences_chart
from source.pages.sidebar_dengue_all_serotypes import choose_colour_dengue
from source.pages.tables import variant_summary_table as vst


def main():
    st.set_page_config(
        page_title="Climade Africa Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="img/cropped-ceri_branco-01-150x150.png"
    )

    st.markdown(css_changes, unsafe_allow_html=True)
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    ## Getting the data
    df_africa = load_data('data/dengue/metadata-all-serotypes.csv')

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
    df_count = sd.new_build_df_count(df_africa)
    df_count_country = sd.new_build_df_count(df_africa, country=True)

    variants_percentage, pivot_df = sd.new_build_variant_percentage(df_count)
    
    # Building percentage dataframe
    #ariants_percentage = sd.build_variant_percentage_df(df_count)

    ###############################################################
    ###############################################################
    ###############################################################

    ### Filter and reset buttons ###
    btn_col_1, btn_col_2 = st.sidebar.columns(2)
    if btn_col_1.button("Reset filters", key='button_reset_filters'):
        sd.reset_filters(df_africa)

    if btn_col_2.button("Filter data", key='button_filter'):
        df_africa = sd.filter_df_africa(countries_choice, lineages_choice, start_date, end_date, df_africa)
        df_count = sd.new_build_df_count(df_africa)
        variants_percentage, pivot_df = sd.new_build_variant_percentage(df_count)


    ###############################################################
    ###############################################################
    ###############################################################

    # End of sidebar
    # Metrics
    sd.show_metrics(df_africa)

    # st.sidebar.header("Acknowledgment")
    # sd.acknowledgment_section(logo_path='img/gisaid_logo.png', link='https://www.gisaid.org/')

    # Add title and subtitle to the main interface of the app
    main_title( "DENGUE VIRUS ALL SEROTYPES - AFRICA DASHBOARD" ,display_countries)

    ### Layout of main pages
    c1, c2 = st.columns((1.5, 1.9))

    ############ First column ###############
    ############## MAP CHART ################
    
    c1.subheader("Genomes per country")
    map_option = c1.selectbox(
        'Metric',
        ('Total number of genomes', 'Genomes by serotype'
         # 'Variants proportion'
         ))
    if map_option == 'Total number of genomes':
        # df_count_countries = sd.new_build_df_count(df_africa, country=True);
        colorpath_africa_map(df_count_country, column=c1, color_pallet="sunsetdark")
    elif map_option == 'Genomes by serotype':
        # Multiselect to choose variants to show
        voc_selected = c1.selectbox("Choose Serotype to show", dengue_variants)
        df_count_map = sd.new_build_df_count(df_africa[df_africa['variant'] == voc_selected], True)
        colorpath_africa_map(df_count_map, column=c1, color_pallet=vocs_color_pallet.get(voc_selected))
    # elif map_option == 'Variants proportion':
    #     c1.write(variants_percentage.head())
    #     scatter_africa_map(variants_percentage, column=c1, map_count_column='Count')

    ############ Second column ###############
    ####### Circulating lineages CHART ###########
    variants_bar_plot(variants_percentage, c2, "Circulating Serotypes", pivot_df, choose_colour_dengue)

    ####### COUNTRIES WHITH SEQUENCE CHART #########
    countries_with_sequences_chart(df_count_country, c2, "Serotype", "Genomes per serotype")

if __name__ == "__main__":
    main()
