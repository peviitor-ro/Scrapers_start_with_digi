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

    if job_type == 'hybrid':
        return job_type
    elif job_type == 'remote':
        return job_type
    else:
        return 'on-site'
