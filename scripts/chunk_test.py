from urb3d.pipeline.utils import run_script

# run_script('chunk_dataset.py',
#            '--input',
#            '.\\data\\birmingham_blocks\\cambridge_block_17.ply',
#            '--output',
#            '.\\data\\birmingham_blocks\\test_chunked')
#
# run_script('segmentation.py',
#            '--ckpt',
#            '.\\models\\really_weighted.ckpt',
#            '--input',
#            '.\\data\\birmingham_blocks\\test_chunked',
#            '--chunked',
#            'y',
#            '--output',
#            '.\\data\\birmingham_blocks\\segmented_cloud.ply')

# run_script('segmentation.py',
#            '--ckpt',
#            '.\\models\\really_weighted.ckpt',
#            '--input',
#            '.\\data\\birmingham_blocks\\birmingham_block_7_subsampled_test.ply',
#            '--output',
#            '.\\data\\birmingham_blocks\\segmented_cloud2.ply')

run_script('pcd_coloring.py',
           '--input',
           '.\\data\\birmingham_blocks\\segmented_cloud.ply',
           '--output',
           '.\\data\\birmingham_blocks\\colored_cloud.ply')