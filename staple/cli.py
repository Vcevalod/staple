# -*- coding: utf-8 -*-

"""Console script for staple."""
import sys
import click

import SimpleITK as sitk
from staple import STAPLE, get_images

@click.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
@click.argument('output_file', nargs=1, type=click.Path())
@click.option('--verbose/--no-shout', default=False)
def main(input_files, output_file, verbose):
    """Run STAPLE algorithm on a set of binary expert segmentations."""
    images = get_images(input_files)
    arrays = [sitk.GetArrayFromImage(image) for image in images]
    staple = STAPLE(arrays, verbose=verbose)
    output_array = staple.run()
    click.echo(f'Sensitivities: {staple.sensitivity.flatten()}')
    click.echo(f'Specificities: {staple.specificity.flatten()}')
    output_image = sitk.GetImageFromArray(output_array)
    one_image = images[0]
    output_image.SetSpacing(one_image.GetSpacing())
    output_image.SetOrigin(one_image.GetOrigin())
    output_image.SetDirection(one_image.GetDirection())
    sitk.WriteImage(output_image, output_file)
    return 0



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
