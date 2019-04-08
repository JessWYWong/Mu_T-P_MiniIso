# Tag-and-Probe Utilities

This repository holds a set of utilities/macros to work with Tag-and-Probe (TnP) ntuples.

All script are written in python and take a `--help` argument, which describes the functionality of the different scripts. The following sections explain the usage in simple use-cases. All of them should work with a setup CMS software (CMSSW) environment.

## Programs: Manipulating and printing TnP trees

### Compare TnP trees

The script `compareTrees` can be used to check that the output ROOT files of different CMSSW package versions is still the same. Run following example to examine the output of the script.

```bash
# Take the example tree, remove the eta branch and set all values of the pt branch to zero
./modifyTree examples/TnPTree.root modifiedTree.root --remove eta --branch pt

# Now, examine the differences using the 'compareTrees' tool
./compareTrees modifiedTree.root examples/TnPTree.root
```
### Skim TnP tree

With the program `skimTree`, you can reduce TnP ROOT files by applying cuts on a specified input tree and copy the result to an output ROOT file. As well, you can remove branches from the tree completely. This is mainly done to reduce the file size and therefore to reduce the needed processing time for TnP studies. Note, that you can load multiple files at once from your local storage device or EOS and merge them together in the output.

```bash
# Skim a tree only with a cut string
./skimTree examples/TnPTree.root skimmedTree.root --cut "tag_IsoMu20==1 && tag_pt>30"

# Remove some specific branches from a tree
./skimTree examples/TnPTree.root skimmedTree.root --remove "tag_* pt eta abseta"

# Remove all branches from the tree except the specified ones
# Here, first you remove all of the branches and re-add only the desired ones
./skimTree examples/TnPTree.root skimmedTree.root --remove "*" --keep "pt eta"

# Load multiple files from local device and EOS and merge them together
# Of course, it is still possible to apply cuts or remove branches
./skimTree "examples/TnPTree.root root://eoscms.cern.ch//eos/cms/path/to/file.root" mergedTree.root
```

### Print TnP tree

You can print run, luminosity and event of a TnP tree with a specified cut. This is used mainly to feed the output to [this CMS tool](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookPickEvents). Most likely, you want to pipe the output to a file.

```bash
# Print output to the terminal (stdout)
./printTree examples/TnPTree.root --cut "tag_IsoMu20==1 && tag_pt>30"

# Write output to file
./printTree examples/TnPTree.root --cut "tag_IsoMu20==1 && tag_pt>30" > outputFile
```

### Create cut string from JSON file

The script `jsonToCut` generates a valid cut string from a JSON file, which specifies runs and luminosity sections (see `examples/cut.json`). Following example shows how you can feed the cut string into the other scripts without doing copy past in the terminal.

```bash
# Read the example JSON file to a shell variable
CUT=$(./jsonToCut examples/cut.json)

# Have a look at the cut string
echo $CUT

# Then, feed the cut to any other program, which takes a cut string
# Note, that you have to put "" around the variable
./printTree examples/TnPTree.root --cut "$CUT"
```

As well, you can combine multiple cuts using this approach. Here a combination of cuts created from a JSON file and a cut from a string.

```bash
# Declare cut from JSON file to as shell variable
CUT1=$(./jsonToCut examples/cut.json)

# Get cut from string
CUT2="tag_IsoMu20==1 && tag_pt>30"

# Combine the cuts with a && operation
# Note, that you have to use () around the variables to get the desired logic!
./printTree examples/TnPTree.root --cut "($CUT1) && ($CUT2)"
```

### Add weight branch to MC TnP tree

Often, a MC TnP tree has to be reweighted with the number of primary vertices (pile-up) to match the data, e.g., if you are measuring an efficiency ratio of MC versus data. This can be done using this program, which copies the input MC files and writes them to the output with an additional weight branch based on the ratio `numVtxData/numVtxMC`.

```bash
./addNVtxWeight "fileData1 fileData2 ..." "fileMC1 fileMC2 ..." filenameOutput.root
```

### Add new branch to TnP tree from an expression

Here, you can add a new branch to a TnP tree using an expression. E.g., you want to cut on a variable, which is not present in the tree, but it is calculable with available variables, then you can use this tool to generate the new branch. Because this feature is not directly supported by ROOT, the given expression has to have following form: `"EXPRESSION;USED_VARIABLE_1;USED_VARIABLE_2;..."` Note, that you can use numpy in the expression, because it is wrapped to a Python statement. Have a look at following examples.

```bash
# We recreate the abseta branch using eta
# You can check the result afterwards using ROOT's TBrowser
./addBranch "examples/TnPTree.root" outputTree.root "abs(eta);eta" absetaNew

# You can even use numpy in the expression
./addBranch "examples/TnPTree.root" outputTree.root "numpy.log10(pt);pt" ptLog10

# Here some random, but complicated, expression
./addBranch "examples/TnPTree.root" outputTree.root "numpy.sqrt(pt*abs(eta))**3;pt;eta" randomVar
```

## Programs: Plotting and publishing results

### Make (nice looking) efficiency plots

With this program, you can generate nice looking, ROOT-like and CMS-approvable plots of TnP efficiencies. The plot contains the efficiency vs a binned variable, e.g., pt or abseta, and you can superimpose multiple graphs. The plots can be done batchwise by defining the free parameters in a JSON config, e.g., `examples/configPlot.json`. To run the configuration, feed the JSON file to the script. Run following example to examine the output.

```bash
./makeEffPlot examples/configEffPlot.json
```

### Make ratio plots

To compare MC and data TnP efficiencies, it is useful to plot a ratio combined with the data itself. This can be done using the `makeRatioPlot` script, which is controlled by a JSON config file, e.g., `examples/configRatioPlot.json`. To run the configuration, feed the JSON file to the script as argument.

```bash
./makeRatioPlot examples/configRatioPlot.json
```

### Make histograms from TnP trees

The program `makeHistPlots` can produce histograms from TnP trees. It can be used the same way the `Draw()` method from `TTree` works, but produces more nicely looking results. Such as the above presented plot programs, it has to be feeded with a JSON config file, e.g., `examples/configHistPlot.json'. Please note that only 1D histograms are supported.

```bash
./makeHistPlot examples/configHistPlot.json
```

### Publish directory as a web page

The program `publishDir` copies a given file, e.g, the `index.php` file from this repository, recursively into a given directory. Then, it is easily browsable through a web browser, if the directory is accessed through a web server such as Apache. You can do this as CERN user, follow [this link](https://espace.cern.ch/webservices-help/websitemanagement/ManagingWebsitesAtCERN/Pages/WebsitecreationandmanagementatCERN.aspx) for more information. Following example shows an use-case in combination with the `makeRatioPlot` tool.

```bash
# Create plots
./makeRatioPlot examples/configRatioPlot.json

# Make them accessable through a PHP web page
./publishDir exampleRatio index.php

# Now, you need to copy the 'exampleRatio' folder to a directory,
# which is accessible by the web server.
```

## Helpful tips and tricks

### Write outputs to file

Remember, all programs do not have a specific option to write the output to a file because this can be done directly in the terminal.

```bash
./someProgram > outputFile
```

### Access data directly from EOS

Because the input and output files are handled by `TFile` classes from ROOT, you can access data directly from EOS. Especially, this is useful for copying a skimmed version of a ROOT file from EOS to your local storage device. All you have to do is giving the EOS path of the file with a `root://` prefix to the script. Have a look at the following example.

```bash
# Copy a skimmed version of a ROOT file on EOS with only the 'pt' branch
./skimTree root://eoscms.cern.ch//eos/cms/path/to/file.root skimmedTree.root --remove "*" --keep "pt"
```

### Make the programs accessible in terminal

To make the programs accessible from every directory on your system, you have to add the repository path to you `PATH` environment variable. Note, that you can attach this line to your `.bashrc` config in your home directory.

```bash
export PATH=$PATH:/path/to/TnPUtils
```
