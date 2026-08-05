# Running

All command line options are documented [here](cmdline.md)

## Making datacards

Once you have written your own inputfile, e.g., `input.yaml`, as shown in the [examples](https://github.com/key4hep/k4GeneratorsConfig/tree/main/examples), execute the following:

```
k4GeneratorsConfig --make --yaml input.yaml
```

This will create a directory containing the desired runcards for event generation in the default directory `Run-Cards`. The directory can be set as well:
```
k4GeneratorsConfig --yaml input.yaml --outputDir /path/to/out
```
overriding settings in the `input.ymal`

## Running Event Generation

The event generation step can be run as well:
```
k4GeneratorsConfig --generate --outputDir /path/to/out
```

or restricted to a specific generator:
```
k4GeneratorsConfig --generate --generator NameOfGenerator --outputDir /path/to/out
```

## Generation summary

A summary of the cross sections for each process and center of mass energy as well as figures with comparisons between the generators are
produced through:
```
k4GeneratorsConfig --summary --outputDir /path/to/out
```

## All Steps

All steps, i.e., creating datacards, running event generation and producing the summary figures, can be performed in a single call:
```
k4GeneratorsConfig --all --outputDir /path/to/out
```


