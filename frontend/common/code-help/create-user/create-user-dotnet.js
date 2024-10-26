module.exports = (
  envId,
  { FEATURE_NAME, FEATURE_NAME_ALT, USER_ID },
  userId,
) => `using Flagsmith;

static FlagsmithClient _flagsmithClient;
_flagsmithClient = new("${envId}");

// Identify the user
var flags = await _flagsmithClient.GetIdentityFlags("${userId || USER_ID}");

// get the state / value of the user's flags 
var isEnabled = await flags.IsFeatureEnabled("${FEATURE_NAME}");
var featureValue = await flags.GetFeatureValue("${FEATURE_NAME_ALT}");
`
