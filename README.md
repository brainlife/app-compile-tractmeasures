<h1 align="center">Compile tractmeasures</h1>

<p align="center">
  One group-level table from the per-subject tract measures of a whole project, with subject, session and tag columns added.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.683"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.683-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT license"></a>
</p>

> **This branch, `tractmeasures-non-dsistudio-v1.0`, is the brainlife.io App Compile tractmeasures csvs across project into one dataframe** ([doi:10.25663/brainlife.app.683](https://doi.org/10.25663/brainlife.app.683)). The other Apps in this repository are listed under **Versions on brainlife.io** below.

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Concatenates tractmeasures csv files from many subjects into one csv, adding subject, session, tag and datatype-tag columns with pandas; a group-analysis utility.**

Reads each input tractmeasures csv, adds subjectID, sessionID, tags and datatype_tags columns from the brainlife input metadata when they are missing, and stacks all rows into output/tractmeasures.csv. Use it to build one dataframe of tract profiles or measures across a project; for DSI Studio tractmeasures use the DSI Studio-specific App.

| | |
|---|---|
| **Inputs** | `neuro/tractmeasures` |
| **Outputs** | `neuro/tractmeasures` |
| **Container** | `brainlife/freesurfer-stats:1.2` |
| **Resources** | 2 CPUs · 0.5 h walltime |
| **Run it** | [doi.org/10.25663/brainlife.app.683](https://doi.org/10.25663/brainlife.app.683) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `tractmeasures` | `neuro/tractmeasures` | yes | tractmeasures csv files of several subjects/sessions (one per input). |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `output` | `neuro/tractmeasures` | Single csv (tractmeasures.csv) with all input rows plus subjectID, sessionID, tags and datatype_tags columns. |

<!-- brainlife-app:end -->

## Versions on brainlife.io

This repository hosts three Apps, each built from its own branch. They do the same job, stacking per-subject tables into one, for different kinds of tract measures.

| App | Input | Branch | Run it | Status |
|---|---|---|---|---|
| **Compile tractmeasures csvs across project into one dataframe** (this branch) | `neuro/tractmeasures` (csv) | [`tractmeasures-non-dsistudio-v1.0`](https://github.com/brainlife/app-compile-tractmeasures/tree/tractmeasures-non-dsistudio-v1.0) | [doi:10.25663/brainlife.app.683](https://doi.org/10.25663/brainlife.app.683) | current |
| Compile measures from dsistudio tractmeasures datatype | `neuro/dsistudio/tractmeasures` | [`tracts-v1.0`](https://github.com/brainlife/app-compile-tractmeasures/tree/tracts-v1.0) | [doi:10.25663/brainlife.app.436](https://doi.org/10.25663/brainlife.app.436) | available |
| Compile qc data from tractmeasures (tsv) data | `dsistudio/tractmeasure` (QC tsv) | [`qc-v1.0`](https://github.com/brainlife/app-compile-tractmeasures/tree/qc-v1.0) | [doi:10.25663/brainlife.app.432](https://doi.org/10.25663/brainlife.app.432) | available |

- **tractmeasures csvs** (`tractmeasures-non-dsistudio-v1.0`): concatenates the csv files of any `neuro/tractmeasures` datasets (for example tract profiles) and adds `subjectID`, `sessionID`, `tags` and `datatype_tags` columns when they are missing.
- **DSI Studio tractmeasures** (`tracts-v1.0`): reads the per-tract DSI Studio statistics files (`*.stat.txt`) of each subject into a table of measures by tract; tracts with a `*.no_result.txt` file get `NaN`.
- **DSI Studio QC** (`qc-v1.0`): stacks DSI Studio QC tsv files into one tsv.

All three are written in Python with [pandas](https://pandas.pydata.org/) and only reshape the tables; they do not change the values.

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.683](https://doi.org/10.25663/brainlife.app.683) (or one of the other versions above), select the tractmeasures datasets of all the subjects and sessions you want to combine and press **Execute**. The compiled table is archived to your project as a single dataset (tagged `group_analysis` for the csv App, `compiled` for the DSI Studio Apps), ready for group statistics.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/). `main` runs the Python script inside the `brainlife/freesurfer-stats:1.2` container; without Singularity, install Python 3 with pandas.

1. Clone this repository and check out the App's branch, for example `git checkout tractmeasures-non-dsistudio-v1.0`.
2. Create `config.json`. The Apps read the subject, session and tags of each input from the `_inputs` list that brainlife.io writes into `config.json`, so a local config needs it too. For the csv App:

   ```json
   {
       "csv": [
           "/input/sub-01/tractmeasures.csv",
           "/input/sub-02/tractmeasures.csv"
       ],
       "_inputs": [
           { "meta": { "subject": "01", "session": "1" }, "tags": [], "datatype_tags": [] },
           { "meta": { "subject": "02", "session": "1" }, "tags": [], "datatype_tags": [] }
       ]
   }
   ```

   The two DSI Studio Apps take a list of input directories under the key `tractmeasures` instead of `csv`.

3. Run the App:

   ```bash
   ./main
   ```

## Outputs

| App | Output |
|---|---|
| tractmeasures csvs | `output/tractmeasures.csv`: all input rows plus `subjectID`, `sessionID`, `tags` and `datatype_tags` columns |
| DSI Studio tractmeasures | `tractmeasures/tractmeasure.tsv`: one row per measure and subject, one column per tract, plus `subjectID`, `sessionID` and `tags` |
| DSI Studio QC | `tractmeasures/tractmeasure.tsv`: all input rows plus `subjectID`, `sessionID` and `tags` |

## Troubleshooting

- **`something failed. checked logs`** (csv App): `output/tractmeasures.csv` was not written. Check the log for a pandas error reading one of the input csv files.

## Citing

> [!TIP]
> If you use this App in your work, please cite the App, the software it builds on and brainlife.io (below). GitHub's **Cite this repository** button gives the App citation in APA and BibTeX.

- Yeh F-C. Shape analysis of the human association pathways. *NeuroImage* (2020).
- Compile tractmeasures csvs across project into one dataframe. brainlife.io App. [doi:10.25663/brainlife.app.683](https://doi.org/10.25663/brainlife.app.683)
- Fischl. FreeSurfer. *NeuroImage* 62:774-781 (2012). [doi:10.1016/j.neuroimage.2012.01.021](https://doi.org/10.1016/j.neuroimage.2012.01.021)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- Brad Caron

**Contributors:** Soichi Hayashi

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io is publicly funded, and acknowledging that support helps keep it running. This App was developed with support from Wellcome, the U.S. National Institutes of Health (including the BRAIN Initiative BRAIN CONNECTS program: The Axonal Projectome EXchange, U24NS140384, and the Center for Mesoscale Connectomics, UM1NS132207) and the U.S. National Science Foundation.</sub>

## License

[MIT](LICENSE), Copyright (c) 2020 brainlife.io, The University of Texas at Austin and Indiana University.
