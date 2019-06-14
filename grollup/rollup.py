import csv
import statistics


def get_sample_list(args):

    samples = []

    with open(args.design_matrix) as dm_file:
        reader = csv.DictReader(dm_file, delimiter='\t')
        for row in reader:
            samples.append(row['sample'])
    return samples


def main(args):

    protein_dict = {}

    samples = get_sample_list(args)

    with open(args.input) as in_file:
        reader = csv.DictReader(in_file, delimiter='\t')
        for row in reader:
            proteins = row['accession'].split(',')
            for protein in proteins:
                if protein not in protein_dict:
                    protein_dict[protein] = []
                protein_dict[protein].append(row)

    #print(len(protein_dict.keys()))

    for protein, rows in protein_dict.items():
        #print(protein, len(rows))
        if len(rows) > 0:
            max_data_points = 0
            all_values = []
            for row in rows:
                data = [row[sample] for sample in samples]
                used_data = len(data) - data.count('NA')
                if used_data > max_data_points:
                    max_data_points = used_data
                all_values += [float(val) for val in data if val != 'NA']

            minimum_intensity = min(all_values)
            maximum_intensity = max(all_values)


            reference = {}
            for max_id, row in enumerate(rows):
                data = [row[sample] for sample in samples]
                used_data = len(data) - data.count('NA')
                #print(len(used_data))
                if used_data == max_data_points:
                    reference[max_id] = row

            if len(reference) > 0:
                total_intensity = 0
                greatest_id = 0
                for max_id, row in reference.items():
                    data = []
                    for sample in samples:
                        if row[sample] != 'NA':
                            data.append(float(row[sample]))

                    intensity_sum = sum(data)
                    if intensity_sum > total_intensity:
                        total_intensity = intensity_sum
                        greatest_id = max_id
                reference_data = []
                for sample in samples:
                    if reference[greatest_id][sample] != 'NA':
                        reference_data.append(float(reference[greatest_id][sample]))
                print(statistics.mean(reference_data), minimum_intensity, maximum_intensity)


