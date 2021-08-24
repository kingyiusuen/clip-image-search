import pandas as pd
from download_unsplash import DATASET_PATH, DOWNLOADED_PHOTOS_PATH
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

import clip_image_search.utils as utils
from clip_image_search import CLIPFeatureExtractor, Searcher


class UnsplashDataset(Dataset):
    def __init__(self):
        super().__init__()
        self.photo_files = list(DOWNLOADED_PHOTOS_PATH.glob("*.jpg"))
        df = pd.read_csv(DATASET_PATH / "photos.tsv000", sep="\t", usecols=["photo_id", "photo_image_url"])
        self.id_to_url = {photo_id: photo_image_url for photo_id, photo_image_url in df.values.tolist()}

    def __len__(self):
        return len(self.photo_files)

    def __getitem__(self, idx):
        photo_file = self.photo_files[idx]
        photo_id = photo_file.name.split(".")[0]
        image = utils.pil_loader(photo_file)
        photo_image_url = self.id_to_url[photo_id]
        return photo_id, photo_image_url, image


def collate(batch):
    return zip(*batch)


def generate_data():
    dataset = UnsplashDataset()
    dataloader = DataLoader(dataset, batch_size=64, shuffle=False, collate_fn=collate)
    feature_extractor = CLIPFeatureExtractor()

    for batch in tqdm(dataloader):
        photo_ids, photo_image_urls, images = batch
        image_features = feature_extractor.get_image_features(images)
        batch_size = len(photo_ids)
        for i in range(batch_size):
            yield {
                "_index": "image",
                "_id": photo_ids[i],
                "url": photo_image_urls[i],
                "feature_vector": image_features[i],
            }


def main():
    searcher = Searcher()

    print("Creating an index...")
    searcher.create_index()

    print("Indexing images...")
    searcher.bulk_ingest(generate_data(), chunk_size=128)


if __name__ == "__main__":
    main()
