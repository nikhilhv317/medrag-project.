# Cleaning log

- patients: removed test/dummy records: 5
- patients: normalised name whitespace/case: 654
- patients: normalised gender values: 694
- patients: cleared impossible future date of birth: 66
- patients: merged duplicate registrations (same MRN): 311
- studies: removed duplicate rows: 1,416
- studies: re-pointed to merged patient: 632
- studies: removed orphans (unknown patient): 558
- studies: normalised modality names: 29,221
- studies: normalised priority values: 2,761
- studies: removed missing / future study dates: 1,102
- reports: stripped HTML markup: 2,687
- reports: removed empty reports: 884
- reports: normalised status values: 2,768
- reports: removed duplicate reports per study: 1,369
- ai_analysis: converted percent confidence to 0-1: 2,602
- ai_analysis: cleared invalid confidence: 800
- studies: without a report after cleaning: 854