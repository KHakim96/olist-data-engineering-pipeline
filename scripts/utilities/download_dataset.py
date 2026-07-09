from pathlib import Path
import shutil

import kagglehub


def main():
    print("=" * 60)
    print("Downloading Olist Dataset...")
    print("=" * 60)

    dataset_path = Path(
        kagglehub.dataset_download(
            "jayeshsalunke101/brazilian-ecommerce-public-dataset"
        )
    )

    destination = Path("data/raw")
    destination.mkdir(parents=True, exist_ok=True)

    print(f"\nDownloaded to:\n{dataset_path}\n")

    for file in dataset_path.glob("*.csv"):
        shutil.copy(file, destination / file.name)
        print(f"Copied: {file.name}")

    print("\nDownload completed successfully.")
    print(f"CSV files saved to: {destination.resolve()}")


if __name__ == "__main__":
    main()