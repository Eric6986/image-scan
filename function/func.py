import io
import json
import logging
from fdk import response
import oci
import os

# Handler method
def handler(ctx, data: io.BytesIO = None):
    logger = logging.getLogger()
    try:
        signer = oci.auth.signers.get_resource_principals_signer()
        object_storage_client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
        ai_vision_client = oci.ai_vision.AIServiceVisionClient({}, signer=signer)

        if os.getenv("COMPARTMENT_OCID") is not None:
            compartment_ocid = os.getenv('COMPARTMENT_OCID')
            logger.info("Configuration key COMPARTMENT_OCID is set..." + compartment_ocid)
        else:
            raise ValueError("ERROR: Missing configuration key COMPARTMENT_OCID ")

        if os.getenv("NAMESPACE_NAME") is not None:
            namespace = os.getenv('NAMESPACE_NAME')
            logger.info("Configuration key NAMESPACE_NAME is set..." + namespace)
        else:
            raise ValueError("ERROR: Missing configuration key  NAMESPACE_NAME ")

        if os.getenv("INPUT_STORAGE_BUCKET") is not None:
            input_storage_bucket = os.getenv('INPUT_STORAGE_BUCKET')
            logger.info("Configuration key INPUT_STORAGE_BUCKET is set..." + input_storage_bucket)
        else:
            raise ValueError("ERROR: Missing configuration key  INPUT_STORAGE_BUCKET ")


        logger.info("Start list image object..")
        objecs_list = object_storage_client.list_objects(namespace, input_storage_bucket)


        object_names = [b.name for b in objecs_list.data.objects]
        # expense_metadata = get_metadata_object_content()
        # expense_report_id = create_expense_header(expense_metadata, admin_credential)

        for x in object_names:
            object_name = str(x)
            logger.info("The object name is .." + object_name)
            # Analyze all files other than metadata.json in object storage
            # vision_json = analyze_using_vision(object_name)
            # logger.info("The object name is .." + object_name)


            analyze_response = ai_vision_client.analyze_image(
                analyze_image_details=oci.ai_vision.models.AnalyzeImageDetails(
                    image=oci.ai_vision.models.ObjectStorageImageDetails(
                        source="OBJECT_STORAGE",
                        namespace_name=namespace,
                        bucket_name=input_storage_bucket,
                        object_name=object_name),
                    features=[
                        oci.ai_vision.models.ImageObjectDetectionFeature(
                        feature_type="OBJECT_DETECTION",
                        max_results=300)],
                    compartment_id=compartment_ocid,
                )
            )

        analysis = json.loads(str(analyze_response.data))
        logger.info(analysis)

        return response.Response(ctx, response_data=analyze_response.data)


    except (Exception, ValueError) as ex:
        logger.info(str(ex))
