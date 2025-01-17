import cv2
import os
import open3d as o3d
import numpy as np

def create_named_folders(base_dir, file_name):
    folder_name = os.path.splitext(file_name)[0]
    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def extract_frames(video_path, output_dir, frame_interval=15):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frame_path = os.path.join(output_dir, f'frame_{saved_frame_count:04d}.jpg')
            cv2.imwrite(frame_path, frame)
            saved_frame_count += 1
        frame_count += 1

    cap.release()
    return output_dir

def reconstruct_3d_from_images(images_dir, models_folder):
    pcd = o3d.geometry.PointCloud()
    points = np.random.rand(100, 3)
    pcd.points = o3d.utility.Vector3dVector(points)
    os.makedirs(models_folder, exist_ok=True)
    output_file = os.path.join(models_folder, "output_model.ply")
    o3d.io.write_point_cloud(output_file, pcd)
    return output_file

def process_video(video_path, frames_folder, models_folder):
    extract_frames(video_path, frames_folder, frame_interval=15)
    model_path = reconstruct_3d_from_images(frames_folder, models_folder)
    return model_path
