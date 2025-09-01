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

👉 Use the `--filter` parameter to filter resource list by a substring, showing only matching entries.

---

### `terraform-champ init`

Scans all subdirectories starting from the current directory for folders containing `main.tf`, prompts you to select which ones to initialize, and then runs `terraform init` in each selected directory.

👉 Use the `--upgrade` flag to also update provider and module configurations.

---

### `terraform-champ apply` (TODO)

Scans all subdirectories starting from the current directory for folders containing `main.tf`, prompts you to select which ones to initialize, and then runs `terraform apply` in each selected directory.
