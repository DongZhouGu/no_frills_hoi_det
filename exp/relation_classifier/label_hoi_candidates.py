import h5py
import utils.io as io
from utils.constants import save_constants


def load_gt_dets(anno_list_json,global_ids):
    global_ids_set = set(global_ids)

    # Load anno_list
    print('Loading anno_list.json ...')
    anno_list = io.load_json_object(anno_list_json)

    gt_dets = {}
    for anno in anno_list:
        if anno['global_id'] not in global_ids_set:
            continue

        global_id = anno['global_id']
        gt_dets[global_id] = {}
        for hoi in anno['hois']:
            hoi_id = hoi['id']
            gt_dets[global_id][hoi_id] = []
            for human_box_num, object_box_num in hoi['connections']:
                human_box = hoi['human_bboxes'][human_box_num]
                object_box = hoi['object_bboxes'][object_box_num]
                det = {
                    'human_box': human_box,
                    'object_box': object_box,
                }
                gt_dets[global_id][hoi_id].append(det)

    return gt_dets


def match_hoi(pred_det,gt_dets):
    is_match = False
    for gt_det in gt_dets:
        human_iou = compute_iou(pred_det['human_box'],gt_det['human_box'])
        if human_iou > 0.5:
            object_iou = compute_iou(pred_det['object_box'],gt_det['object_box'])
            if object_iou > 0.5:
                is_match = True
                break

    return is_match


def main(exp_const,data_const):
    io.mkdir_if_not_exists(exp_const.exp_dir)

    print('Saving constants ...')
    save_constants({'exp':exp_const,'data':data_const},exp_const.exp_dir)

    print(f'Reading hoi_candidates_{exp_const.subset}.hdf5 ...')
    hoi_cand_hdf5 = h5py.File(data_const.hoi_cand_hdf5,'r')

    print(f'Creating hoi_candidate_labels_{exp_const.subset}.hdf5 ...')
    filename = os.path.join(
        exp_const.exp_dir,
        f'hoi_candidates_{exp_const.subset}.hdf5')
    hoi_cand_label_hdf5 = h5py.File(filename,'w')

    print('Loading gt hoi detections ...')
    split_ids = os.path.join(data_const.split_ids_json)
    global_ids = split_ids[exp_const.subset]
    gt_dets = load_gt_dets(data_const.anno_list_json,global_ids)

    print('Loading hoi_list.json ...')
    hoi_list = io.load_json_object(data_const.hoi_list_json)
    hoi_ids = [hoi['id'] for hoi in hoi_list]

    for global_id in global_ids:
        boxes_scores_rpn_ids = hoi_cand_hdf5[global_id]['boxes_scores_rpn_ids']
        start_end_ids = hoi_cand_hdf5[global_id]['start_end_ids']
        row_to_roi_id = {}
        for hoi_id in hoi_ids:
            start_id,end_id = start_end_ids[int(hoi_id)-1]
            for i in range(start_id,end_id):
                row_to_roi_id[i] = hoi_id

        cand_det = {
            'human_box': boxes_scores_rpn_ids[]
        }
