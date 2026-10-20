# Tangency Labs benchmark models

Openly licensed CAD and mesh models in open, standard formats, for benchmarking how CAD and CAE
software imports, tessellates and meshes them. Everything here is released under
[CC0-1.0](LICENSE): anyone can use, change and share it for any purpose, with no attribution
required.

## Only non-proprietary models

Every model in this repository must be free of proprietary rights and restrictions. Before you
add a model, check all of the following:

- **You have the right to release it under CC0-1.0.** You made it yourself, or its author
  already released it under CC0-1.0. Models under any other licence, CC-BY included, are not
  accepted, because the repository has one licence for every file.
- **It is not confidential.** No customer, employer or client parts, no parts under NDA, no
  export-controlled designs.
- **It is not someone else's product or brand.** No copies of commercial products, logos or
  trademarked shapes.
- **It does not come from a dataset or model site with its own terms.** That includes ABC, MAMBO,
  Thingi10K, GrabCAD, Thingiverse and vendor sample libraries, even when the files can be
  downloaded freely.
- **It is in an open format.** Use one of the folders below. Native formats of commercial CAD
  systems (`.prt`, `.sldprt`, `.catpart`, `.ipt`, `.f3d`, `.x_t`, `.sat`, …) are not accepted.

A pull request that does not meet these rules is closed. If you later find that a model here
breaks them, open an issue and it will be removed.

## Formats

| Folder | Format | Standard | Kind |
|---|---|---|---|
| [`step/`](step/) | STEP (`.step`, `.stp`) | ISO 10303-21 (AP203, AP214, AP242) | B-rep CAD |
| [`iges/`](iges/) | IGES (`.iges`, `.igs`) | IGES 5.3 (ANSI/US PRO) | B-rep and surface CAD |
| [`3mf/`](3mf/) | 3MF (`.3mf`) | 3MF Consortium core specification | Triangle mesh |
| [`stl/`](stl/) | STL (`.stl`), ASCII or binary | De facto standard | Triangle mesh |
| [`obj/`](obj/) | Wavefront OBJ (`.obj`) | Published open format | Polygon mesh |
| [`gltf/`](gltf/) | glTF 2.0 (`.gltf`, `.glb`) | ISO/IEC 12113 (Khronos) | Polygon mesh and scene |
| [`ply/`](ply/) | PLY (`.ply`) | Published open format | Polygon mesh, point cloud |

If you need another open format, open an issue to propose a folder for it.

## Adding a model

Each model has its own folder inside the folder for its format:

```
step/
  bracket-l-angle/
    bracket-l-angle.step
    README.md
```

The model's `README.md` records:

- **Name** and a one-line description.
- **Author**, so others can credit them (CC0 does not require it, but it is good practice).
- **Made with**: the software and version that wrote the file, and the export settings
  (for example the STEP application protocol or the STL chord tolerance).
- **Size**: bodies, faces, edges for B-rep files, or triangles and vertices for meshes.
- **Why it is interesting**: what it stresses (many small faces, tight fillets, thin walls,
  large assemblies, bad tolerances, very fine tessellation, …).
- **SHA-256** of the model file, so benchmark results can name the exact file they used.

By opening a pull request you confirm that you have the right to release its files and you
release them under CC0-1.0.

Keep each file under 50 MB; GitHub refuses files over 100 MB. Use folder and file names in lower
case with hyphens. The same model can appear in several formats, one folder in each, and each
folder's README links to the others.

## Sharing benchmark results

Share how long a model takes to load in your software, and on what machine. Add a file to
[`results/`](results/) by pull request, starting from
[`results/TEMPLATE.md`](results/TEMPLATE.md). Results from any software are welcome, open source
or commercial, as long as you are allowed to publish them; some commercial licences forbid
publishing benchmarks.

So that results can be compared, give for each run:

- **The model**: its path in this repository and its SHA-256.
- **The software**: name, version, and the import settings (healing, tessellation tolerance,
  units).
- **The machine**: CPU model, cores and threads, RAM, GPU and driver, storage (SSD or HDD),
  operating system and version.
- **What you timed**: from where to where (for example "file open command to first frame drawn"
  or "import call returns"), and whether the file was cold or already in the OS cache.
- **The times**: the median of at least 3 runs, plus the minimum and maximum. Give peak memory if
  you can measure it.

## Disclaimer

The files are provided as is, without warranty, liability or indemnity, and Tangency Labs and the
contributors accept no responsibility for any harmful or unlawful use of them: read
[DISCLAIMER.md](DISCLAIMER.md). The models are benchmark test data, not engineering designs, and
benchmark results are the submitters' own measurements, published as submitted and not verified
or endorsed by Tangency Labs.

## Licence

Every file in this repository, models included, is released under
[CC0-1.0](LICENSE) (Creative Commons Zero 1.0 Universal).
