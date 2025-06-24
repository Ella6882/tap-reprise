# tap-reprise

`tap-reprise` is a Singer tap for Reprise. Reprise offers specific API endpoints that provide detailed data on viewer interactions and consumption patterns within your demos.

Currently, the Reprise API supports two products, Reprise Replay and Reprise Replicate:

Reprise Replay requires
- 1 authentication token 
- 1 API endpoint (replay_session_activity)

Reprise Replicate requires
- 1 authentication token 
- 1 API endpoint (API_Replicate_Analytics)

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

Install from GitHub:

```bash
pipx install git+https://github.com/Ella6882/tap-reprise.git@main
```

-->

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-reprise --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

The instructions to create a token for the Reprise Replay Data API, based on the provided Zendesk article can be found [here](https://reprise.zendesk.com/hc/en-us/articles/18940321925659-Replay-Data-API).

The instructions to create a token for the Reprise Replicate Data API, based on the provided Zendesk article can be found [here](https://reprise.zendesk.com/hc/en-us/articles/28931374746907-Replicate-Data-API).

You will need to provide the token (Replay and Replicate), client_id, and start_timestamp (format: YYYY-MM-DD HH:MM:SS) to use the tap. There is an optional end_timestamp (format: YYYY-MM-DD HH:MM:SS) that can be configured as well.

Due to a 100MB data limit per API request, we fetch data in daily intervals.

```
{
    "client_id": "",
    "start_timestamp": "2025-06-20 00:00:00",
    "replay_token": "",
    "replicate_token": ""
}
```

## Usage

You can easily run `tap-reprise` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-reprise --version
tap-reprise --help
tap-reprise --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

Prerequisites:

- Python 3.8+
- [uv](https://docs.astral.sh/uv/)

```bash
uv sync
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
uv run pytest
```

You can also test the `tap-reprise` CLI interface directly using `uv run`:

```bash
uv run tap-reprise --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-reprise
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-reprise --version

# OR run a test ELT pipeline:
meltano run tap-reprise target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
