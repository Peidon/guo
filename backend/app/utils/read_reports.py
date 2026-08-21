import opendataloader_pdf

if __name__ == '__main__':

    # Batch all files in one call — each convert() spawns a JVM process, so repeated calls are slow
    opendataloader_pdf.convert(
        input_path=["VAL.pdf"],
        output_dir="output/",
        format="json,markdown",
        image_output="off"
    )

