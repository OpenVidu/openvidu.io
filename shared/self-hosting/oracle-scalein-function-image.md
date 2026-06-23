## Using your own scale-in function image

By default, the OCI Function pulls the scale-in image published by OpenVidu in the Madrid OCIR (`mad.ocir.io`). If you prefer to host the image in your own OCI Registry — for example, to avoid cross-region pulls, comply with internal policies, or pin a customised build — you can build and push it yourself, then point the `scale_in_function_image` variable to your image.

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

5. Update `terraform.tfvars` with the new image reference:

    ```hcl
    scale_in_function_image = "<region-key>.ocir.io/<tenancy-namespace>/scale-in-function:<tag>"
    ```

!!! info
    Make sure the OCI Function's compartment has the IAM policies needed to pull from the target repository. If the repository lives in a different tenancy from the OCI Function, see [Pulling Images from Repositories in other Tenancies :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionspullingimagescrosstenancy.htm){:target=_blank} for the required Endorse/Admit/Define policy statements.
