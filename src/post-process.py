# Simple post-processing script to create a clean subset of tree data
#     - JRz, for personal use and not indended for real-world applications

#  NOTE: This is eliminating valid, useful data in lieu of something easier to visualize
#        It's possible that this will mask trends, as it is often VERY likely that missing data are non-randomly distributed (e.g. more missing data pre-1955 in this dataset)


import csv

def valid_species(species):
    return len(species) > 2 and "Tree(s) ::" not in species and ':: Tree' != species

def valid_location(latitude, longitude):
    return len(latitude) > 1 and len(longitude) > 1 and is_float(latitude) and is_float(longitude)

def valid_site_info(site_info):
    return len(site_info) > 0 and site_info != ":"

def valid_dbh(dbh):
    return len(dbh) > 0 and is_float(dbh)

def valid_plot_size(plot_size):
    plot_size = plot_size.lower()
    if "x" in plot_size:
        dimen = plot_size.split('x')
        length = (dimen[0].strip())
        width = (dimen[1].strip())
        if is_float(length) and is_float(width) and float(length) > 0 and float(width) > 0:
            return True
    elif "width" in plot_size and "ft" in plot_size:
        width = plot_size[6:-2]
        if is_float(width) and float(width) > 0:
            return True
    return False

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def passes_filter(row):
    return valid_location(row['Latitude'], row['Longitude']) and \
        valid_dbh(row['DBH']) and \
            valid_plot_size(row['PlotSize'])
    

# import and run passes_filter
data = []
header = []
with open('./static/Street_Tree_List-2022-01-30_RAW.csv','r') as f:
    reader = csv.DictReader(f)
    
    header = reader.fieldnames
    for row in reader:
        if passes_filter(row):
            # you might consider doing some additional processing here
            # e.g. splitting up qSpecies
            data.append(row)

print(len(data))

# export to new CSV       
with open('./static/Street_Tree_List-2022-01-30_FILTERED.csv','w') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)
