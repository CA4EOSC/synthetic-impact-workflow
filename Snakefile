#report: "report/workflow.rst"

rule all:
    input:
        "data/capacity_fits.nc",
        "data/linear_reg_coeffs.txt"
    shell:
        "synthetic-ca4eosc-workflow --make-visualisation"

rule retrieve_datasets:
    output:
        "data/tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_18500116-19141216.nc",
        "data/tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_19500116-20141216.nc"
    shell:
        "synthetic-ca4eosc-workflow --retrieve-data"

rule make_deviations:
    input:
        "data/tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_18500116-19141216.nc",
        "data/tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_19500116-20141216.nc"
    output:
        "data/deviations.nc"
    shell:
        "synthetic-ca4eosc-workflow --make-deviations"
 
rule make_population:
    input:
        "data/deviations.nc"
    output:
        "data/populations.nc"
    shell:
        "synthetic-ca4eosc-workflow --make-population"

rule fit_capacities:
    input:
        "data/deviations.nc",
        "data/populations.nc"
    output:
        "data/capacity_fits.nc"
    shell:
        "synthetic-ca4eosc-workflow --fit-capacities"

rule make_regression:
    input:
        "data/capacity_fits.nc"
    output:
        "data/linear_reg_coeffs.txt"
    shell:
        "synthetic-ca4eosc-workflow --make-regression"

rule make_visualisation:
    input:
        "data/capacity_fits.nc",
        "data/linear_reg_coeffs.txt"
    shell:
        "synthetic-ca4eosc-workflow --make-visualisation"
