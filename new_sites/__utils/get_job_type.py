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
        case 'remote':
            return job_type
        case 'hybrid':
            return job_type
        case _:
            return 'on-site'
