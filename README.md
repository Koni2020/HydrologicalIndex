# streamflow-signatures

A Python toolkit for calculating annual streamflow signatures from daily discharge time series.

This repository provides the custom code used to derive annual hydrological indices from daily streamflow data. The calculated indicators include flow magnitude, high-flow and low-flow frequency, event duration, timing, variability, rise/fall rates, and baseflow-related metrics.

## Repository description

**Repository name:** `streamflow-signatures`

**Description:**
A Python toolkit for calculating annual streamflow signatures from daily discharge data, including flow magnitude, high/low-flow frequency and duration, timing, variability, rise/fall rates, and baseflow index.

## Purpose

This code was developed to support reproducible hydrological data processing for a Scientific Data submission. It converts daily streamflow records into annual streamflow signature metrics that can be used for hydrological characterization, trend analysis, inter-basin comparison, and technical validation of streamflow-related datasets.

## Main functions

The repository includes functions for:

* Identifying consecutive non-missing streamflow segments.
* Calculating the average duration of high-flow, low-flow, and zero-flow events.
* Calculating the half-streamflow timing index.
* Calculating the Richards-Baker flashiness index.
* Separating baseflow using the Eckhardt digital filter.
* Computing annual streamflow signature metrics from daily discharge data.

## Input data

The main function expects daily streamflow data as a `pandas.DataFrame`.

Required format:

* Rows: daily dates.
* Index: `pandas.DatetimeIndex`.
* Columns: station names, grid IDs, basin IDs, or other streamflow series identifiers.
* Values: daily streamflow or discharge.

Example input structure:

```text
date        station_001  station_002  station_003
1981-01-01      12.35       18.42       10.21
1981-01-02      11.87       17.96       10.05
1981-01-03      13.02       18.11       10.44
...
```

## Output data

The function returns a `pandas.DataFrame` containing annual streamflow signatures.

The output rows correspond to years, and the output columns correspond to calculated hydrological indicators.

Main output indicators include:

### Flow magnitude

* `Qmax1`: annual maximum 1-day mean streamflow
* `Qmax3`: annual maximum 3-day mean streamflow
* `Qmax7`: annual maximum 7-day mean streamflow
* `Qmax30`: annual maximum 30-day mean streamflow
* `Qmax90`: annual maximum 90-day mean streamflow
* `Qmin1`: annual minimum 1-day mean streamflow
* `Qmin3`: annual minimum 3-day mean streamflow
* `Qmin7`: annual minimum 7-day mean streamflow
* `Qmin30`: annual minimum 30-day mean streamflow
* `Qmin90`: annual minimum 90-day mean streamflow
* `Qmean`: annual mean streamflow

### Flow quantiles

* `Q1st`: annual 1st percentile streamflow
* `Q5th`: annual 5th percentile streamflow
* `Q10th`: annual 10th percentile streamflow
* `Q25th`: annual 25th percentile streamflow
* `Q50th`: annual median streamflow
* `Q75th`: annual 75th percentile streamflow
* `Q90th`: annual 90th percentile streamflow
* `Q95th`: annual 95th percentile streamflow
* `Q99th`: annual 99th percentile streamflow

### Monthly flow magnitude

* `Qmean1` to `Qmean12`: mean streamflow for January to December in each year.

### High-flow and low-flow frequency

* `FreH`: frequency of high-flow days
* `FreL`: frequency of low-flow days
* `FreZ`: frequency of zero-flow days
* `Fre1st`: frequency of extremely low-flow days below the 1st percentile
* `Fre5th`: frequency of low-flow days below the 5th percentile
* `Fre95th`: frequency of high-flow days above the 95th percentile
* `Fre99th`: frequency of extremely high-flow days above the 99th percentile

### Number of flow events

* `NumH`: number of high-flow days
* `NumL`: number of low-flow days
* `NumZ`: number of zero-flow days
* `Num1st`: number of days below the 1st percentile
* `Num5th`: number of days below the 5th percentile
* `Num95th`: number of days above the 95th percentile
* `Num99th`: number of days above the 99th percentile

### Flow duration

* `DurH`: average duration of high-flow events
* `DurL`: average duration of low-flow events
* `DurZ`: average duration of zero-flow events
* `Durl1st`: average duration of extremely low-flow events below the 1st percentile
* `Dur5th`: average duration of low-flow events below the 5th percentile
* `Dur95th`: average duration of high-flow events above the 95th percentile
* `Dur99th`: average duration of extremely high-flow events above the 99th percentile

### Flow timing

* `HFD`: half-streamflow date
* `MMD`: date of annual maximum daily streamflow
* `MC7DF`: date of annual minimum 7-day mean streamflow

### Flow variability and flashiness

* `RM`: annual range between maximum and minimum streamflow
* `BM`: annual range of baseflow
* `VY`: annual variance of streamflow
* `COVY`: annual coefficient of variation
* `QCV`: quantile-based coefficient of variation
* `RMM`: ratio between median flow and annual maximum 1-day flow
* `RBFI`: Richards-Baker flashiness index

### Rise and fall rates

* `RRmean`: mean positive daily flow change
* `RRmedian`: median positive daily flow change
* `FRmean`: mean negative daily flow change
* `FRmedian`: median negative daily flow change

### Baseflow-related metrics

* `BFI`: baseflow index
* `BM`: annual baseflow range

## Requirements

The code was written in Python and requires the following packages:

```text
numpy
pandas
numba
baseflow
```

Recommended installation:

```bash
pip install numpy pandas numba baseflow
```

## Usage

Example:

```python
import pandas as pd
from streamflow_signatures import main_compute

# Read daily streamflow data
sf = pd.read_csv(
    "daily_streamflow.csv",
    index_col=0,
    parse_dates=True
)

# Calculate annual streamflow signatures
signatures = main_compute(sf)

# Save output
signatures.to_csv("annual_streamflow_signatures.csv")
```

## Method overview

Daily streamflow data are first organized by calendar year. Annual flow magnitude indicators are calculated using rolling windows of 1, 3, 7, 30, and 90 days. Flow quantiles are calculated for each year. High-flow and low-flow thresholds are defined using streamflow percentiles and relative thresholds. Consecutive high-flow, low-flow, and zero-flow periods are identified to calculate event duration.

Baseflow is separated using the Eckhardt digital filter with the following parameters:

```text
a = 0.925
BFImax = 0.8
b_LH = first streamflow value
```

The annual baseflow index is then calculated as the ratio between annual mean baseflow and annual mean streamflow.

## File structure

Recommended repository structure:

```text
streamflow-signatures/
│
├── README.md
├── LICENSE
├── requirements.txt
├── streamflow_signatures.py
├── examples/
│   ├── example_input.csv
│   └── example_usage.py
└── outputs/
    └── annual_streamflow_signatures_example.csv
```

## Reproducibility

To reproduce the streamflow signature calculation:

1. Prepare daily streamflow data as a CSV file with dates as the first column.
2. Install the required Python dependencies.
3. Run the example script or call `main_compute()` directly.
4. Export the returned annual signature table as CSV or another preferred format.

Example command:

```bash
python examples/example_usage.py
```

## Data availability

The input streamflow data used in the associated study should be deposited in an appropriate public data repository. The data availability statement in the manuscript should include the repository name, DOI or accession number, file names, and a brief explanation of the data structure.

Placeholder statement:

```text
The daily streamflow data and derived annual streamflow signature datasets associated with this study are available from [repository name] at [DOI/accession number]. The repository includes the original daily streamflow input files, processed annual streamflow signature tables, and metadata describing the variables and file structure.
```

## Code availability

The custom Python code used to calculate annual streamflow signatures is available in this repository. The code includes functions for calculating flow magnitude, frequency, duration, timing, variability, flashiness, and baseflow-related hydrological indicators from daily streamflow time series.

Placeholder statement:

```text
The custom Python code used to calculate annual streamflow signatures is available at [GitHub repository URL] and archived at [Zenodo DOI]. The repository includes source code, dependency information, example input data, and example scripts for reproducing the annual hydrological indicators reported in this study.
```

## License

Please specify the license before public release.

Recommended open-source license:

```text
MIT License
```

or

```text
Apache License 2.0
```

## Citation

If you use this code, please cite the associated Scientific Data article and the archived software release.

Placeholder citation:

```text
Author(s). Year. streamflow-signatures: A Python toolkit for calculating annual streamflow signatures from daily discharge data. Zenodo. DOI: [DOI]
```

## Contact

For questions about the code or data processing workflow, please contact:

```text
[Your name]
[Your institution]
[Your email]
```
