import numpy as np

# To Do expand to HST/COSMOS imaging using hyperspectral plotting techniques
# (ex. reduce N band images to 3 bands by PCA, etc)
# To Do automatically calculate band scales by incorporating filter curves


def _lupton_intensity(image, int_type="mean", **kwargs):
    """Multicolor intensity as defined in Lupton (2004)

    Parameters
    ----------
    image : `~numpy.ndarray`
        Array of shape (nobj, npix, npix, nchans)
    int_type : string
        mean, sum or rms of the input channels as the intensity

    Returns
    -------
    `~numpy.ndarray`
        A combined measure of pixel intensities
    """

    if int_type == "mean":
        return np.mean(image, axis=-1)
    elif int_type == "sum":
        return np.sum(image, axis=-1)
    elif int_type == "rms":
        return np.sqrt(np.mean(np.square(image), axis=-1))


def _lupton_stretch(I, Q, stretch, stretch_type="lupton", minimum=0, **kwargs):
    """stretch based scaling of the combined image

    Parameters
    ----------
    I : `~numpy.ndarray`
        output of the function _lupton_intensity
    Q : float
        asinh softening parameter
    stretch : float
        The linear stretch parameter
    stretch_type : str, optional
        The type of scaling function to use, lupton, lupton_sqrt or marshal, by default "lupton"
    minimum : float, optional
        The ofset to use for the lupton stretchings
    Returns
    -------
    `~numpy.ndarray`
        The scaling image after the stretching
    To Do
    -----
    Add zscale based scaling to as in astropy
    """

    if stretch_type == "lupton":
        return np.arcsinh(Q * (I - minimum) / stretch) / Q
    if stretch_type == "lupton_sqrt":
        return np.sqrt(np.arcsinh(Q * (I - minimum) / stretch) / Q)
    if stretch_type == "marshal":
        return np.arcsinh(Q * I / stretch) / (Q * I)


def _lupton_saturate(r, g, b, threshold, **kwargs):

    x = numpy.dstack((r, g, b))

    # Highest pixel-value at given position
    maxpix = numpy.max(x, axis=-1)
    maxpix[maxpix < 1.0] = 1.0

    rr = r / maxpix
    gg = g / maxpix
    bb = b / maxpix

    return rr, gg, bb


def _offset(image, offset=0, **kwargs):
    """
    Add an arbitrary offset to the final scaled image
    Args:
    image (array): Array of shape (nobj, npix, npix, nchans)
    offset (float or array of shape nchans): Add a constant value to whole image or add offset channel wise
    """
    return image + offset


def _scale_channels(scales):
    assert len(scales) == 3
    s1, s2, s3 = scales
    mean = (s1 + s2 + s3) / 3.0
    return s1 / mean, s2 / mean, s3 / mean
    return image * scale


def make_lupton_rgb(
    image_r,
    image_g,
    image_b,
    minimum=0,
    stretch=5,
    Q=8,
    filename=None,
    backsub=False,
    scales=(1.0, 1.0, 1.0),
):

    if backsub:
        image_r = subtract_background(image_r)
        image_g = subtract_background(image_g)
        image_b = subtract_background(image_b)
    rscale, gscale, bscale = _normalize_scales(scales)

    red.apply_scale()
    green.apply_scale()
    blue.apply_scale()

    I = humvi.lupton_intensity(red.image, green.image, blue.image, type="sum")
    stretch = humvi.lupton_stretch(I, Q, alpha)

    # Apply stretch to channel images:
    r = stretch * red.image
    g = stretch * green.image
    b = stretch * blue.image
    r, g, b = humvi.pjm_mask(r, g, b, masklevel)
    r, g, b = humvi.pjm_offset(r, g, b, offset)

    if saturation == "color":
        # Saturate to colour at some level - might as well be 1, since
        # Q redefines scale?:
        threshold = 1.0
        r, g, b = humvi.lupton_saturate(r, g, b, threshold)
