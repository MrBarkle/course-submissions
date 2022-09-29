#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

// New Sorting Function prototypes
void mergesort(pair arr[], int l, int r);
void merge(pair arr[], int l, int m, int r);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // Loop over array of candidates
    for (int i = 0; i < candidate_count; i++)
    {
        // If user voted for valid candidate
        if (strcmp(candidates[i], name) == 0)
        {
            // Update vote preference
            ranks[rank] = i;
            return true;
        }
    }
    // Return false if invalid vote was cast
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    
    int left; 
    int right;
    
    // Terrible triple for loop. O(n3)
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            // preferences diagonal case when comparing candidate i = 0 to candidate j = 0
            if (i != j)
            {
                for (int k = 0; k < candidate_count; k++)
                {
                    // Find the rank of i
                    if (ranks[k] == i)
                    {
                        left = k;
                    }
                    // Find the rank of j
                    else if (ranks[k] == j)
                    {
                        right = k;
                    }
                }
                
                if (left < right)
                {
                    // If candidate i beats candidate j, increment preference
                    preferences[i][j] ++;    
                }
                
            }
            
        }
        
    }

}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // Loop through preferences 2D array
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i; j < candidate_count; j++)
        {
            // If not a diagonal case where self vs self 
            if (preferences[i][j] != preferences[j][i])
            {
                // Compare i vs j else j vs i for winner and loser
                if (preferences[i][j] > preferences[j][i])
                {
                    pairs[pair_count].winner = i;
                    pairs[pair_count].loser = j;
                    pair_count ++;
                }
                else
                {
                    pairs[pair_count].winner = j;
                    pairs[pair_count].loser = i;
                    pair_count ++;
                }
            }
        }
    }
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // Use a version of merge sort to sort pairs 
    mergesort(pairs, 0, pair_count - 1);
}

// Merge two 'pair' type subarrays of arr[]
void merge(pair arr[], int l, int m, int r)
{
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;
    
    // Temp arrays
    pair L[n1], R[n2];
    
    // Copy data to temp arrays
    for (i = 0; i < n1; i++)
    {
        L[i].winner = arr[l + i].winner;
        L[i].loser = arr[l + i].loser;
    }
    for (j = 0; j < n2; j++)
    {
        R[j].winner = arr[m + 1 + j].winner;
        R[j].loser = arr[m + 1 + j].loser;
    }
    
    // Merge temp arrays back into arr[l..r]
    i = 0; // Initial index of first subarray
    j = 0; // Initial index of second subarray
    k = l; // Initial index of merged subarray
    while (i < n1 && j < n2)
    {
        // Looking at the strength of victory for each pair 
        int sov1 = (preferences[L[i].winner][L[i].loser] - preferences[L[i].loser][L[i].winner]);
        int sov2 = (preferences[R[j].winner][R[j].loser] - preferences[R[j].loser][R[j].winner]);
        // Sort highest strength of victory first
        if (sov1 >= sov2)
        {
            arr[k].winner = L[i].winner;
            arr[k].loser = L[i].loser;
            i++;
        }
        else
        {
            arr[k].winner = R[j].winner;
            arr[k].loser = R[j].loser;
            j++;
        }
        k++;
    }
    // Copy remaining elements of L[], if any
    while (i < n1)
    {
        arr[k].winner = L[i].winner;
        arr[k].loser = L[i].loser;
        i++;
        k++;
    }
    // Copy remaining elements of R[], if any 
    while (j < n2)
    {
        arr[k].winner = R[j].winner;
        arr[k].loser = R[j].loser;
        j++;
        k++;
    }
}

// Merge sort for pair type array
void mergesort(pair arr[], int l, int r)
{
    if (l < r)
    {
        int m = l + (r - l) / 2;
        // Sort halves recursively 
        mergesort(arr, l, m);
        mergesort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // Loop through each pair in pairs[]
    for (int i = 0; i < pair_count; i ++)
    {
        // Pair has yet to be locked
        if (locked[pairs[i].winner][pairs[i].loser] == false)
        {
            int curr = pairs[i].winner;
            int target = pairs[i].loser;
            int j = 0;
            bool skip = false;
            
            // Loop through ancestors of current vertex
            while (j < candidate_count)
            {
                // If the current vertex has an ancestor at j 
                while (locked[j][curr] == true && j != curr)
                {
                    // Was it the target of curr? (loser in pair where j is winner)
                    if (j == target)
                    {
                        // If so, break; this creates cycle
                        skip = true;
                        break;
                    }
                    else
                    {
                        // Increment j and keep looking at ancestors and who they beat
                        curr = j;
                        j = 0;
                    }
                }
                j++;
            }
            // Lock or skip?
            if (skip == false)
            {
                locked[pairs[i].winner][pairs[i].loser] = true;
            }
        }
    }
}

// Print the winner of the election
void print_winner(void)
{
    int candidate;
    bool winner = false;
    // Loop over the columns of locked
    for (int i = 0; i < candidate_count; i++)
    {
        // Looking at each row of a column 
        for (int j = 0; j < candidate_count; j++)
        {
            // If an entire column is false, thats the winner
            if (locked[j][i] == true)
            {
                winner = false;
                break;
            }
            else
            {
                winner = true;
            }
        }
        if (winner == true)
        {
            // Set winner
            candidate = i;  
        }
        
    }
    printf("%s\n", candidates[candidate]);
}

