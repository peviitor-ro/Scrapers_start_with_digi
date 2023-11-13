#
#
#
# Function to get type of job;
#
#

def get_job_type(job_type: str) -> str:
    '''
    ... this func return job type in automation mode;
    '''
    job_type = job_type.lower()

    match job_type:
        case 'Remote':
            return job_type
        case 'Hybrid':
            return job_type
        case _:
            return 'On-site'
