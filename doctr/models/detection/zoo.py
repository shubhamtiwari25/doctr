# Copyright (C) 2021-2022, Mindee.

# This program is licensed under the Apache License version 2.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0.txt> for full license details.

from typing import Any, List

from doctr.file_utils import is_tf_available, is_torch_available

from .. import detection
from ..preprocessor import PreProcessor
from .predictor import DetectionPredictor

__all__ = ["detection_predictor"]

ARCHS: List[str]
ROT_ARCHS: List[str]


if is_tf_available():
    ARCHS = ['db_resnet50', 'db_mobilenet_v3_large', 'linknet_resnet18', 'linknet_resnet34', 'linknet_resnet50']
    ROT_ARCHS = ['linknet_resnet18_rotation']
elif is_torch_available():
    ARCHS = ['db_resnet34', 'db_resnet50', 'db_mobilenet_v3_large', 'linknet_resnet18',
             'linknet_resnet34', 'linknet_resnet50']
    ROT_ARCHS = ['db_resnet50_rotation']


def _predictor(
    arch: str,
    pretrained: bool,
    assume_straight_pages: bool = True,
    **kwargs: Any
) -> DetectionPredictor:

    if arch not in ARCHS:
        raise ValueError(f"unknown architecture '{arch}'")

    if arch not in ROT_ARCHS and not assume_straight_pages:
        raise AssertionError("You are trying to use a model trained on straight pages while not assuming"
                             " your pages are straight. If you have only straight documents, don't pass"
                             f" assume_straight_pages=False, otherwise you should use one of these archs: {ROT_ARCHS}")

    # Detection
    _model = detection.__dict__[arch](pretrained=pretrained, assume_straight_pages=assume_straight_pages)
    kwargs['mean'] = kwargs.get('mean', _model.cfg['mean'])
    kwargs['std'] = kwargs.get('std', _model.cfg['std'])
    kwargs['batch_size'] = kwargs.get('batch_size', 1)
    predictor = DetectionPredictor(
        PreProcessor(_model.cfg['input_shape'][:-1] if is_tf_available() else _model.cfg['input_shape'][1:], **kwargs),
        _model
    )
    return predictor


def detection_predictor(
    arch: str = 'db_resnet50',
    pretrained: bool = False,
    assume_straight_pages: bool = True,
    **kwargs: Any
) -> DetectionPredictor:
    """Text detection architecture.

    >>> import numpy as np
    >>> from doctr.models import detection_predictor
    >>> model = detection_predictor(arch='db_resnet50', pretrained=True)
    >>> input_page = (255 * np.random.rand(600, 800, 3)).astype(np.uint8)
    >>> out = model([input_page])

    Args:
        arch: name of the architecture to use (e.g. 'db_resnet50')
        pretrained: If True, returns a model pre-trained on our text detection dataset
        assume_straight_pages: If True, fit straight boxes to the page

    Returns:
        Detection predictor
    """

    return _predictor(arch, pretrained, assume_straight_pages, **kwargs)
