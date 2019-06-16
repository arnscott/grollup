import statistics





class Protein:

    def __init__(self, external_id: str = '', samples: list = []):
        self.external_id = external_id
        self.peptides = []
        self.samples = samples

    def set_rollup_reference(self):

        max_data_points = 0
        all_values = []
        for peptide in self.peptides:
            data = [peptide[sample] for sample in self.samples]
            used_data = len(data) - data.count('NA')
            if used_data > max_data_points:
                max_data_points = used_data
            all_values += [float(val) for val in data if val != 'NA']

        self.minimum_intensity = min(all_values)
        self.maximum_intensity = max(all_values)

        reference = {}
        for max_id, row in enumerate(self.peptides):
            data = [row[sample] for sample in self.samples]
            used_data = len(data) - data.count('NA')
            # print(len(used_data))
            if used_data == max_data_points:
                reference[max_id] = row


        total_intensity = 0
        greatest_id = 0
        for max_id, row in reference.items():
            data = []
            for sample in self.samples:
                if row[sample] != 'NA':
                    data.append(float(row[sample]))

            intensity_sum = sum(data)
            if intensity_sum > total_intensity:
                total_intensity = intensity_sum
                greatest_id = max_id
        reference_data = {}
        for sample in self.samples:
            if reference[greatest_id][sample] != 'NA':
                reference_data[sample] = float(reference[greatest_id][sample])

        self.reference_mean = statistics.mean([intensity for sample, intensity in reference_data.items()])


    def scale_peptide_intensities(self):

        for peptide in self.peptides:
            for column, data, in peptide.items():
                if column in self.samples:
                    if data == 'NA':
                        peptide[column] = 0.0
                    else:
                        try:
                            scaled_intensity_value = (float(data) - self.reference_mean) / (self.maximum_intensity - self.minimum_intensity)
                            peptide[column] = scaled_intensity_value
                        except ZeroDivisionError as e:
                            print(peptide)
                            print(self.minimum_intensity, self.maximum_intensity)
                            raise e

    def calc_peptide_mean(self):

        sample_data = {sample: [] for sample in self.samples}

        for peptide in self.peptides:
            for column, data in peptide.items():
                if column in self.samples:
                    if data != 0.0:
                        sample_data[column].append(data)

        mean_samples = {}
        for sample, intensities in sample_data.items():
            if len(intensities) != 0:
                mean_samples[sample] = statistics.mean(intensities)
            else:
                return None

        return mean_samples





