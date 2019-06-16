import csv

from grollup.proteins import Protein

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
            data = [row[sample] for sample in samples]
            used_data = len(data) - data.count('NA')
            if used_data > 1:
                proteins = row['accession'].split(',')
                for protein in proteins:
                    if protein not in protein_dict:
                        protein_dict[protein] = Protein(protein, samples)

                    protein_dict[protein].peptides.append(row)

    for external_id, protein in protein_dict.items():
        protein.set_rollup_reference()
        protein.scale_peptide_intensities()


    proteins = {}

    for external_id, protein in protein_dict.items():
        proteins[external_id] = protein.calc_peptide_mean()

    headers = ['protein_id']

    headers += [sample for sample in samples]

    with open(args.output, 'w') as out_file:
        writer = csv.DictWriter(out_file, delimiter='\t', fieldnames=headers)
        writer.writeheader()

        for protein_id, intensities in proteins.items():
            if intensities:
                record = {'protein_id': protein_id}
                record.update(intensities)
                writer.writerow(record)



