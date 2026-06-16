## Publishing the scale-in function image

The OCI Function that performs graceful Media Node scale-in runs from a container image that must be hosted in an [OCI Registry (OCIR) :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryoverview.htm){:target=_blank} in the **same region** as the Function. Because of this regional constraint, the **`scale_in_function_image`** parameter is mandatory: you must make the scale-in image available in an OCIR in your deployment's region and point the parameter to it.

!!! info
    If you are deploying in the **Madrid** region (`mad.ocir.io`), you can skip this section entirely. OpenVidu already publishes the scale-in image in the Madrid OCIR, so you only need to set `scale_in_function_image = "mad.ocir.io/axp2ice0s7el/openvidu-scalein:main"` (the value that was previously used as the default). The steps below are only required when deploying in any other region.

OpenVidu publishes a prebuilt scale-in image on Docker Hub, so there are two ways to get it into your OCIR. Pick the one that best fits your needs:

=== "Option 1: Use the prebuilt image (recommended)"

    Pull the prebuilt image that OpenVidu publishes on Docker Hub and push it, unchanged, to your own OCIR.

    1. Pull the image from Docker Hub:

        ```bash
        docker pull docker.io/openvidu/openvidu-oci-scalein:3.7.0
        ```

    2. Authenticate Docker against your OCI Registry. You will need an [OCI Auth Token :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrygettingauthtoken.htm){:target=_blank} for the user you log in with:

        ```bash
        docker login <region-key>.ocir.io -u '<tenancy-namespace>/<username>' -p '<auth-token>'
        ```

        Replace `<region-key>` with the [OCIR region code :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryprerequisites.htm#regional-availability){:target=_blank} (for example `fra` for Frankfurt, `iad` for Ashburn, `mad` for Madrid).

        Replace `<username>` with the value matching your authentication setup — the exact format depends on whether your tenancy uses identity domains, federation with IDCS, or local IAM users. See [Pushing Images Using the Docker CLI :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrypushingimagesusingthedockercli.htm){:target=_blank} for the exact pattern in each case (typical forms are `<username>`, `<identity-domain>/<username>`, or `oracleidentitycloudservice/<email>`).

    3. Tag the pulled image for your OCIR. The tag must follow the format `<region-key>.ocir.io/<tenancy-namespace>/<repo>:<tag>`:

        ```bash
        docker tag docker.io/openvidu/openvidu-oci-scalein:3.7.0 <region-key>.ocir.io/<tenancy-namespace>/openvidu-oci-scalein:3.7.0
        ```

    4. Push the image to your OCIR:

        ```bash
        docker push <region-key>.ocir.io/<tenancy-namespace>/openvidu-oci-scalein:3.7.0
        ```

    5. Set `scale_in_function_image` in `terraform.tfvars` to the image reference you just pushed:

        ```hcl
        scale_in_function_image = "<region-key>.ocir.io/<tenancy-namespace>/openvidu-oci-scalein:3.7.0"
        ```

=== "Option 2: Build the image from source"

    Build the scale-in function image yourself from the OpenVidu sources and push it to your OCIR — useful if you want to pin or customise the build. This requires the `openvidu-oracle` repository cloned (see [Deployment details](#deployment-details)).

    1. From the cloned `openvidu-oracle` repository, navigate to the scale-in function source directory:

        ```bash
        cd openvidu-oracle/pro/scalein-function
        ```

    2. Authenticate Docker against your OCI Registry. You will need an [OCI Auth Token :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrygettingauthtoken.htm){:target=_blank} for the user you log in with:

        ```bash
        docker login <region-key>.ocir.io -u '<tenancy-namespace>/<username>' -p '<auth-token>'
        ```

        Replace `<region-key>` with the [OCIR region code :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryprerequisites.htm#regional-availability){:target=_blank} (for example `fra` for Frankfurt, `iad` for Ashburn, `mad` for Madrid).

        Replace `<username>` with the value matching your authentication setup — the exact format depends on whether your tenancy uses identity domains, federation with IDCS, or local IAM users. See [Pushing Images Using the Docker CLI :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrypushingimagesusingthedockercli.htm){:target=_blank} for the exact pattern in each case (typical forms are `<username>`, `<identity-domain>/<username>`, or `oracleidentitycloudservice/<email>`).

    3. Build and tag the image. The tag must follow the format `<region-key>.ocir.io/<tenancy-namespace>/<repo>:<tag>`:

        ```bash
        docker build -t <region-key>.ocir.io/<tenancy-namespace>/scale-in-function:<tag> .
        ```

    4. Push the image to OCIR:

        ```bash
        docker push <region-key>.ocir.io/<tenancy-namespace>/scale-in-function:<tag>
        ```

    5. Set `scale_in_function_image` in `terraform.tfvars` to the image reference you just pushed:

        ```hcl
        scale_in_function_image = "<region-key>.ocir.io/<tenancy-namespace>/scale-in-function:<tag>"
        ```

!!! info
    Make sure the OCI Function's compartment has the IAM policies needed to pull from the target repository. If the repository lives in a different tenancy from the OCI Function, see [Pulling Images from Repositories in other Tenancies :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionspullingimagescrosstenancy.htm){:target=_blank} for the required Endorse/Admit/Define policy statements.
