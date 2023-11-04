

<style lang="scss">
    .page {
        padding: 24px;
    }
    .header {
        display: flex;
        flex-direction: row;
        align-items: center;

        a {
            margin-left: auto;
        }
    }

    .title {
        & > .title-subtext {
            padding-left: 16px;
        }
    }

    section {
        // margin-bottom: 2000px;
    }
</style>

<div class="page">
    <div class="header">
        <div class="title">
            <h1 class="title-text">Pi Server</h1>
            <p class="title-subtext">Cole's personal home server.</p>
        </div>

        <a href="login">Login</a>
    </div>



    <div class="body">
        <section id="directory-section">
            <h2>Directory</h2>
            <ul>
                <li><a href="#project-section">Projects</a></li>
                <li><a href="#about-section">About</a></li>
            </ul>
        </section>

        <section id="project-section">
            <h2>Projects Hosted</h2>
            <ul>
                <li><a href="dog-tracker-project">Dog Tracker Project</a></li>
                <!-- <li><a href="meal">Dog Tracker Project</a></li> -->
            </ul>
        </section>

        <section id="about-section">
            <h2>About The Server</h2>
        </section>
    </div>
</div>

