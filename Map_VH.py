def quantity_counts_by_id(data):
    # make a DataFrame with locations for each company
    locations = data.groupby("Identifiant").first()
    locations = locations.loc[:, ["LLX",
                                 "LLY",
                                 "Nom_Etablissement_x", 
                                  "Departement", "Commune"]]
    
    # count quantity for each company
    quantity_counts =  data.groupby('Identifiant')['Quantite'].agg('sum').to_frame()
    quantity_counts.columns= ["Quantite"]
    

    #join quantity and locations
    counts = quantity_counts.join(locations)
    return counts

def plot_station_counts(frame):
    import folium
    # generate a new map
    folium_map = folium.Map(location = [46.7111, 1.7191],
                        zoom_start = 6,
                        tiles = "CartoDB dark_matter", width = "100%")

    # for each row in the data, add a cicle marker
    for index, row in frame.iterrows():
        Quantite = row["Quantite"]
        
        # generate the popup message that is shown on click.
        popup_text = "{}<br> Commune: {}<br> Entreprise: {}<br> Quantite: {} (tonnes/an) "
        popup_text = popup_text.format(row["Departement"], 
                                       row["Commune"],
                                       row["Nom_Etablissement_x"],
                                       row["Quantite"])
        
        # radius of circles
        radius = Quantite/10000
        

        # choose the color of the marker
        if Quantite>0:
            # color="#FFCE00" # orange
            # color="#007849" # green
            color="#E37222" # tangerine
        else:
            # color="#0375B4" # blue
            # color="#FFCE00" # yellow            
            color="#0A8A9F" # teal
        
        # add marker to the map
        folium.CircleMarker(location=(row["LLY"],
                                      row["LLX"]),
                            radius=radius,
                            color=color,
                            popup=popup_text,
                            fill=True).add_to(folium_map)
    return folium_map


def My_map(ets, p0):
    from pyproj import Proj, transform
    
    p1 = Proj(init='epsg:4326')  # longitude / latidude
    p2 = Proj(init='epsg:2192')  # Lambert 93
    
    long, lat = transform(p2, p1, ets.Coordonnees_X.values, ets.Coordonnees_Y.values)
    ets['LLX'] = long
    ets['LLY'] = lat
    
    ets_2 = p0.merge(ets, on = "Identifiant")
    ets_fin = ets_2[["Identifiant", "Nom_Etablissement_x", "Quantite", "Code_Postal", "Commune", "Departement", "Region", 
                   "LLX", "LLY"]]
    
    my_map = quantity_counts_by_id(ets_fin)
    
    return plot_station_counts(my_map)



def My_map_2(names, prod):
    from pyproj import Proj, transform
    p1 = Proj(init='epsg:4326')  # longitude / latidude
    p2 = Proj(init='epsg:2192')  # Lambert 93
    
    long, lat = transform(p2, p1, names.Coordonnees_X.values, names.Coordonnees_Y.values)
    names['LLX'] = long #We transform the coordonates
    names['LLY'] = lat
    
    ets_2 = prod.merge(names, on = "Identifiant")
    ets_fin = ets_2[["Identifiant", "Nom_Etablissement_x", "Quantite", "Code_Postal", "Commune", "Departement", "Region", 
                   "LLX", "LLY"]]
     #We merge the 2 dataframes and we keep only the variables that interest us
    my_map = quantity_counts_by_id(ets_fin)
    
    return my_map