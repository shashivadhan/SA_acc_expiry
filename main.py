name: Deploy Cloud Function

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Authenticate to GCP
        uses: google-github-actions/auth@v1
        with:
          workload_identity_provider: "projects/31239933098/locations/global/workloadIdentityPools/github-pool/providers/github-provider-v2"
          service_account: "github-wif-reporter@guido-460817.iam.gserviceaccount.com"

      - name: Deploy Cloud Function
        uses: google-github-actions/deploy-cloud-functions@v1
        with:
          name: notify-email
          runtime: python311
          entry_point: notify_email
          region: asia-south1
          source_dir: .
          env_vars: |
            EMAIL_USERNAME=${{ secrets.EMAIL_USERNAME }}
            EMAIL_PASSWORD=${{ secrets.EMAIL_PASSWORD }}
            EMAIL_SENDER=${{ secrets.EMAIL_SENDER }}
            EMAIL_RECIPIENTS=${{ secrets.EMAIL_RECIPIENTS }}
