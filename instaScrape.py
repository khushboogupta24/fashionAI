import instaloader

def download_instagram_photos(username):
    # Create an Instaloader object
    L = instaloader.Instaloader()

    try:
        # Retrieve profile metadata
        profile = instaloader.Profile.from_username(L.context, username)

        # Create a folder for the user's photos
        folder_name = f"{username}_photos"
        L.download_profile(profile.username, profile_pic=False)

        print(f"Photos downloaded to folder: {folder_name}")
    except instaloader.exceptions.ProfileNotExistsException:
        print("Profile not found.")

if __name__ == "__main__":
    # Input the Instagram username you want to download photos from
    username = input("Enter the Instagram username: ")

    # Download photos
    download_instagram_photos(username)