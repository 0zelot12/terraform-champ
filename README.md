# terraform-champ

An interactive Terraform CLI wrapper that simplifies terraform workflows.

## Features

### `terraform-champ target`

Runs `terraform plan` and presents an **interactive list of resources that would be changed**.  
You can select which resources to target directly in the CLI.  
After selection, `terraform apply` is executed, and you’ll still be prompted to confirm the changes.

**Disclaimer:** Using `-target` with Terraform is generally discouraged. Only use it when necessary, and refer to the Terraform documentation for more details.

---

### `terraform-champ replace`

Runs `terraform plan` and shows an **interactive list of all resources**.  
You can select which resources should be replaced directly in the CLI.  
After selection, `terraform apply` is executed, and you’ll be prompted to confirm the changes.

👉 Use the `--target` flag if you also want to restrict replacements to specific targets (**feature pending implementation**).

---

### `terraform-champ init`

Scans the project structure and runs `terraform init` in all detected directories.  
By default, all paths are initialized, but you can exclude specific ones if needed.

👉 Use the `--upgrade` flag to also update provider and module configurations.
