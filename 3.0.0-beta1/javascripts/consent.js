var consent = __md_get("__consent")
if (consent && consent.custom) {
  /* The user accepted the cookie */
  console.log("The user accepted the cookie");
} else {
  /* The user rejected the cookie */
  console.log("The user rejected the cookie");

}