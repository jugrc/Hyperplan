from clipper_admin import ClipperConnection, DockerContainerManager

if __name__ == "__main__":
    # Must connect in order to stop all Clipper cluster and all model containers
    clipper_conn = ClipperConnection(DockerContainerManager())
    clipper_conn.connect()

    clipper_conn.stop_all()
